import BloodCell;
import BrainCell;

public class Main{
    BloodCell mainBlood = new BloodCell();
    BrainCell mainBrain = new BrainCell();

    BloodCell secondBlood = mainBlood.clone();
    BrainCell secondBrain = mainBrain.clone();
}