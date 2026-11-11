package bookTrading;

import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.Behaviour;
import jade.core.behaviours.TickerBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

public class BookBuyerAgent extends Agent {
    private String targetBookTitle;
    private AID[] sellerAgents = new AID[0];
    private boolean requestInProgress = false;

    @Override
    protected void setup() {
        Object[] args = getArguments();

        if (args == null || args.length == 0) {
            System.out.println("Book's title not set.");
            doDelete();
            return;
        }

        targetBookTitle = args[0].toString().trim().replaceAll("\\s+", "_");
        System.out.println(getLocalName() + " is looking for a book " + targetBookTitle);

        // Периодически ищем продавцов в DF и отправляем запрос
        addBehaviour(new TickerBehaviour(this, 5000) {
            @Override
            protected void onTick() {
                if (requestInProgress) {
                    return;
                }

                DFAgentDescription template = new DFAgentDescription();
                ServiceDescription sd = new ServiceDescription();
                sd.setType("book-selling");
                template.addServices(sd);

                try {
                    DFAgentDescription[] result =
                            DFService.search(myAgent, template);

                    sellerAgents = new AID[result.length];
                    for (int i = 0; i < result.length; i++) {
                        sellerAgents[i] = result[i].getName();
                    }
                } catch (FIPAException e) {
                    e.printStackTrace();
                    return;
                }

                if (sellerAgents.length == 0) {
                    System.out.println("Yet no buyers have been found.");
                    return;
                }

                requestInProgress = true;
                myAgent.addBehaviour(new RequestPerformer());
            }
        });
    }

    private class RequestPerformer extends Behaviour {
        private int step = 0;
        private int repliesCount = 0;
        private int bestPrice = Integer.MAX_VALUE;
        private AID bestSeller;
        private MessageTemplate template;

        @Override
        public void action() {
            switch (step) {
                case 0: {
                    // Рассылаем CFP всем найденным продавцам
                    ACLMessage cfp = new ACLMessage(ACLMessage.CFP);
                    for (AID seller : sellerAgents) {
                        cfp.addReceiver(seller);
                    }

                    cfp.setContent(targetBookTitle);
                    cfp.setConversationId("book-trade");

                    String replyWith = "cfp-" + System.currentTimeMillis();
                    cfp.setReplyWith(replyWith);
                    myAgent.send(cfp);

                    template = MessageTemplate.and(
                            MessageTemplate.MatchConversationId("book-trade"),
                            MessageTemplate.MatchInReplyTo(replyWith));

                    step = 1;
                    break;
                }

                case 1: {
                    // Собираем предложения и отказы
                    ACLMessage reply = myAgent.receive(template);

                    if (reply == null) {
                        block();
                        return;
                    }

                    if (reply.getPerformative() == ACLMessage.PROPOSE) {
                        try {
                            int price = Integer.parseInt(reply.getContent());

                            if (bestSeller == null || price < bestPrice) {
                                bestPrice = price;
                                bestSeller = reply.getSender();
                            }
                        } catch (NumberFormatException e) {
                            System.out.println("Got incorrect price.");
                        }
                    }

                    repliesCount++;
                    if (repliesCount >= sellerAgents.length) {
                        step = 2;
                    }
                    break;
                }

                case 2: {
                    if (bestSeller == null) {
                        System.out.println("No buyers have the book "
                                + targetBookTitle);
                        step = 4;
                        break;
                    }

                    // Покупаем у продавца с минимальной ценой
                    ACLMessage order =
                            new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);
                    order.addReceiver(bestSeller);
                    order.setContent(targetBookTitle);
                    order.setConversationId("book-trade");

                    String replyWith = "order-" + System.currentTimeMillis();
                    order.setReplyWith(replyWith);
                    myAgent.send(order);

                    template = MessageTemplate.and(
                            MessageTemplate.MatchConversationId("book-trade"),
                            MessageTemplate.MatchInReplyTo(replyWith));

                    step = 3;
                    break;
                }

                case 3: {
                    ACLMessage reply = myAgent.receive(template);

                    if (reply == null) {
                        block();
                        return;
                    }

                    if (reply.getPerformative() == ACLMessage.INFORM) {
                        System.out.println(targetBookTitle
                                + " successfully bought. Price: " + bestPrice);
                        step = 4;
                        myAgent.doDelete();
                    } else {
                        System.out.println("Buyer couldnt make an order");
                        step = 4;
                    }
                    break;
                }

                default:
                    break;
            }
        }

        @Override
        public boolean done() {
            if (step == 4) {
                requestInProgress = false;
                return true;
            }
            return false;
        }
    }

    @Override
    protected void takeDown() {
        System.out.println("Seller " + getLocalName() + " finished work.");
    }
}