public class GameOfLife(){

    public Byte[][] matrix = null;
    public int dimension = 0;
    public int iterations;

    public GameOfLife(int dimension, int iterations){
        this.matrix = new Byte[dimension][dimension];
        this.dimension = dimension;
        this.iterations = iterations;
    }

    public int countNeighboors(int i, int j){
        counter = this.matrix[i - 1][j - 1] +
                this.matrix[i - 1][j] +
                this.matrix[i - 1][j + 1] +
                this.matrix[i][j - 1] +
                this.matrix[i][j + 1] +
                this.matrix[i + 1][j - 1] +
                this.matrix[i + 1][j] +
                this.matrix[i + 1][j + 1]
        return counter;
    }

    public void simulation(){
        for(int k = 1; k <= iterations; k++){
            Byte[][] new_population = new Byte[this.dimension][this.dimension];
            for(int i = 0; i < this.dimension; i++){
                for(int j = 0; j < this.dimension; j++){
                    int neighboors = this.countNeighboors(i, j);
                    if(matrix[i][j] == 1) { 
                        if (neighboors == 2 || neighboors == 3){
                            new_population[i][j] = 1;
                        }
                        else {
                            new_population[i][j] = 0;
                        }
                    }
                    else {
                        if (neighboors == 3){
                            new_population[i][j] = 1;
                        }
                        else {
                            new_population[i][j] = 0;
                        }
                    }    
                }   
            }
            matrix = new_population
            // PRINT board - matrix
        }
    }


}