package bookTrading;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.core.behaviours.OneShotBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

public class BookSellerAgent extends Agent {
    private final Map<String, Integer> catalogue =
            new ConcurrentHashMap<String, Integer>();

    private BookSellerGui gui;

    @Override
    protected void setup() {
        System.out.println("Seller " + getLocalName() + " is ready.");

        gui = new BookSellerGui(this);
        gui.setVisible(true);

        // Регистрируем услугу продавца в DF — «жёлтых страницах»
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());

        ServiceDescription sd = new ServiceDescription();
        sd.setType("book-selling");
        sd.setName("JADE-book-trading");
        dfd.addServices(sd);

        try {
            DFService.register(this, dfd);
        } catch (FIPAException e) {
            e.printStackTrace();
        }

        // Обработка запросов о наличии книги и её цене
        addBehaviour(new CyclicBehaviour(this) {
            @Override
            public void action() {
                ACLMessage msg = myAgent.receive(
                        MessageTemplate.MatchPerformative(ACLMessage.CFP));

                if (msg == null) {
                    block();
                    return;
                }

                String title = msg.getContent();
                Integer price = catalogue.get(title);
                ACLMessage reply = msg.createReply();

                if (price != null) {
                    reply.setPerformative(ACLMessage.PROPOSE);
                    reply.setContent(String.valueOf(price));
                } else {
                    reply.setPerformative(ACLMessage.REFUSE);
                    reply.setContent("not-available");
                }

                myAgent.send(reply);
            }
        });

        // Обработка заказа от покупателя
        addBehaviour(new CyclicBehaviour(this) {
            @Override
            public void action() {
                ACLMessage msg = myAgent.receive(
                        MessageTemplate.MatchPerformative(
                                ACLMessage.ACCEPT_PROPOSAL));

                if (msg == null) {
                    block();
                    return;
                }

                Integer price = catalogue.remove(msg.getContent());
                ACLMessage reply = msg.createReply();

                if (price != null) {
                    reply.setPerformative(ACLMessage.INFORM);
                    reply.setContent("purchased");
                } else {
                    reply.setPerformative(ACLMessage.FAILURE);
                    reply.setContent("not-available");
                }

                myAgent.send(reply);
            }
        });
    }

    // Этот метод вызывается из окна продавца
    public void updateCatalogue(final String title, final int price) {
        addBehaviour(new OneShotBehaviour(this) {
            @Override
            public void action() {
                catalogue.put(title, price);
                System.out.println(myAgent.getLocalName()
                        + " added the book " + title + " for " + price);
            }
        });
    }

    @Override
    protected void takeDown() {
        try {
            DFService.deregister(this);
        } catch (FIPAException e) {
            e.printStackTrace();
        }

        if (gui != null) {
            gui.dispose();
        }

        System.out.println("Seller " + getLocalName() + " finished work.");
    }
}