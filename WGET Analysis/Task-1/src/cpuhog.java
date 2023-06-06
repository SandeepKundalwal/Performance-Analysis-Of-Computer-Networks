public class cpuhog {
    public static void main(String[] args) {
        int iterations = Integer.parseInt(args[0]);
        long start = System.currentTimeMillis();
        for(int i = 0; i < iterations; i++){
            double result = calculateTan(8);
        }
        long end = System.currentTimeMillis();
        System.out.println("Execution Time: " + ((end - start) / 1000f) + "s");
    }

    public static double calculateTan(int baseNumber){
        double result = 0;
        double baseNumberPowered = Math.pow(baseNumber, 7);
        while(baseNumberPowered >= 0){
            result += Math.atan(baseNumberPowered) * Math.tan(baseNumberPowered);
            baseNumberPowered--;
        }
        return result;
    }
}


