public class UniversalControl{

    private TVDevice device; // composition to interface

    public UniversalControl(TVDevice newDevice){
        this.device = newDevice;
    }

    public void turnOn(){
        this.device.turnOn();
    }

    public void turnOff(){
        this.device.turnOff();
    }

    public void increaseVolume(){
        this.device.increaseVolume();
    }

    public void decreaseVolume(){
        this.device.decreaseVolume();
    }

    public void setChannel(int channel){
        this.device.setChannel(channel);
    }
}