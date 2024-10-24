public class TV100SUD extends TVDevice{

    private boolean statusOn = false;
    private int volume = 0;
    private int currentChannel = 1;

    public void turnOn(){
        this.statusOn = true;
        System.out.println("TV100SUD is on");
    }

    public void turnOff(){
        this.statusOn = false;
        System.out.println("TV100SUD is off");
    }

    public void increaseVolume(){
        this.volume += 1;
        System.out.println("Volume: " + this.volume);
    }

    public void decreaseVolume(){
        this.volume -= 1;
        System.out.println("Volume: " + this.volume);
    }

    public void setChannel(int channel){
        this.currentChannel = channel;
        System.out.println("Channel: " + this.currentChannel);
    }
}