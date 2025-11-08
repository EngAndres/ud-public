public interface Pokemon {
    public abstract int attack();

    public abstract Pokemon evolute();

    public abstract void defense(String typeAdversary, int attackValue);

    public abstract void healthRecovery();
}