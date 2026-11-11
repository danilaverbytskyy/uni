
package A;

import jade.core.Agent;
import jade.core.AID;
import jade.core.behaviours.*;
import jade.lang.acl.ACLMessage;

public class AMain extends Agent {

    @Override
    protected void setup() {
        System.out.println("Привет! Агент " + getAID().getName() + " готов.");

        // Поведение для получения ответа
        addBehaviour(new CyclicBehaviour(this) {
            @Override
            public void action() {
                ACLMessage msg = receive();

                if (msg != null) {
                    System.out.println(
                            getLocalName() + " received: " + msg.getContent()
                    );
                } else {
                    block();
                }
            }
        });

        // Поведение для отправки запроса
        addBehaviour(new OneShotBehaviour(this) {
            @Override
            public void action() {
                ACLMessage msg = new ACLMessage(ACLMessage.INFORM);
                msg.addReceiver(new AID("agentb", AID.ISLOCALNAME));
                msg.setLanguage("English");
                msg.setContent("Ping");

                send(msg);

                System.out.println("Агент A отправил: Ping");
            }
        });
    }
}
