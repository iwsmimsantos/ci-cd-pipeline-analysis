namespace Api.Services;

public class CalculatorService
{
    public int Sum(int a, int b)
    {
        return a + b
    }

    public int Divide(int a, int b)
    {
        if (b == 0)
            throw new DivideByZeroException();

        return a / b;
    }

    public double CalculateBMI(double weight, double height)
    {
        return weight / (height * height);
    }
}
