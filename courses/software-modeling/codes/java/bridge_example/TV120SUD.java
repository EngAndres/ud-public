public class TV120SUD extends TVDevice{
    
    private boolean status = false;
    private int currentVolume = 0;
    private final int MAX_VOLUME = 100;
    private final int MIN_VOLUME = 0;
    private int currentChannel = 0;
    
    public void turnOn(){
        if (!status){
            this.status = true;
            System.out.println("TV120SUD is on");
        }
    }

    public void turnOff(){
        if (status){
            this.status = false;
            System.out.println("TV120SUD is off");
        }
    }

    public abstract void increaseVolume(){
        if (status && currentVolume < MAX_VOLUME){
            this.currentVolume += 1;
            System.out.println("Volume Verified: " + this.currentVolume);
        }
    }

    public abstract void decreaseVolume(){
        if (status && currentVolume > MIN_VOLUME){
            this.currentVolume -= 1;
            System.out.println("Volume Verified: " + this.currentVolume);
        }
    }

    public abstract void setChannel(int channel){
        if (status){
            this.currentChannel = channel;
            System.out.println("Channel Verified: " + this.currentChannel);
        }
    }
}