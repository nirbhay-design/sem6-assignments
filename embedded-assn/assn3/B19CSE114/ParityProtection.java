import java.lang.Math;
import java.util.Scanner;   

class Destination{
    String message;
    String response;
    Destination(){
        System.out.println("Destination is waiting for message");
    }
    private boolean checkparity(){
        int calc_parity = 0;
        for (int i = 0;i< this.message.length()-1; i++){
            int parity = this.message.charAt(i) - '0';
            calc_parity = calc_parity ^ parity; 
        }
        int last_parity = this.message.charAt(this.message.length()-1) - '0';
        if (last_parity == calc_parity){
            return true;
        }
        return false;
    }
    public void recv_msg(String message){
        this.message= message;
        boolean checkpar = checkparity();
        if (checkpar){
            response = "message received";
        } else {
            response = "someone has changed the message";
        }
    }
    public String getresponse(){
        return response;
    }
}

class Distribution_channel{
    String message;
    Destination dest;
    Distribution_channel(Destination dest){
        this.dest = dest;
    }
    private void alter_msg(){
        int alter = (int) Math.round((Math.random()));
        if (alter == 1) {
            int genrand = (int) Math.round(Math.random() * (message.length()-2));
            char bit = message.charAt(genrand);
            char[] a = new char[message.length()];
            a = message.toCharArray();    
            if (bit == '1'){
                a[genrand] = '0';
            } else {
                a[genrand] = '1';
            }            
            message = String.valueOf(a);
        }
    }
    public void pass_message(String msg){
        message = msg;
        alter_msg();
        this.dest.recv_msg(message);
    }
}

class Sender{
    String message;
    Distribution_channel dc;
    Sender(){
        System.out.println("sender ready to send data");
    }
    public void send_msg(String msg,Distribution_channel dch){
        dc = dch;
        message = parity_gen(msg);
        // System.out.println("sending msg " + message);
        dc.pass_message(message);
    }
    private String parity_gen(String msg){
        int count_1 = 0;
        for (int i = 0;i<msg.length() ;i++) {
            int byt = msg.charAt(i)-'0';
            if (byt == 1){
                count_1++;
            }
        }
        if ((count_1 & 1) == 0){
           msg = msg + '0'; 
        } else {
            msg = msg + '1';
        }
        return msg;
    }
}

public class ParityProtection{
    public static void main(String args[]){
        Sender sender = new Sender();
        Destination dest = new Destination();
        Distribution_channel dch = new Distribution_channel(dest);
        while (true){
            Scanner sc = new Scanner(System.in);
            System.out.print("enter msg to send: ");
            String msg = sc.nextLine();
            sender.send_msg(msg,dch);
            String res = dest.getresponse();
            System.out.println(res);
        }
    }
}