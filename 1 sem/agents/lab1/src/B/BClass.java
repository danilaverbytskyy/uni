
package B;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;

public class BClass extends Agent {

    @Override
    protected void setup() {
        System.out.println("Привет! Агент " + getAID().getName() + " готов.");

        addBehaviour(new CyclicBehaviour(this) {
            @Override
            public void action() {
                ACLMessage msg = receive();

                if (msg != null) {
                    System.out.println(
                            getLocalName() + " received: " + msg.getContent()
                    );

                    ACLMessage reply = msg.createReply();
                    reply.setPerformative(ACLMessage.INFORM);
                    reply.setContent("Pong");

                    send(reply);

                    System.out.println("Агент B отправил: Pong");
                } else {
                    block();
                }
            }
        });
    }
}
