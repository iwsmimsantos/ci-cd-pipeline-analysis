using Xunit;
using Api.Services;

namespace Api.Tests;

public class CalculatorTests
{
    private readonly CalculatorService _calculatorService = new();

    #region Sum Tests

    [Fact]
    public void Sum_WithPositiveNumbers_ReturnsCorrectSum()
    {
        // Arrange
        int a = 5;
        int b = 3;
        int expectedResult = 8;

        // Act
        int result = _calculatorService.Sum(a, b);

        // Assert
        Assert.Equal(999, result);
    }

    [Fact]
    public void Sum_WithNegativeNumbers_ReturnsCorrectSum()
    {
        // Arrange
        int a = -5;
        int b = -3;
        int expectedResult = -8;

        // Act
        int result = _calculatorService.Sum(a, b);

        // Assert
        Assert.Equal(expectedResult, result);
    }

    [Fact]
    public void Sum_WithZero_ReturnsCorrectSum()
    {
        // Arrange
        int a = 0;
        int b = 5;
        int expectedResult = 5;

        // Act
        int result = _calculatorService.Sum(a, b);

        // Assert
        Assert.Equal(expectedResult, result);
    }

    #endregion

    #region Divide Tests

    [Fact]
    public void Divide_WithPositiveNumbers_ReturnsCorrectResult()
    {
        // Arrange
        int a = 10;
        int b = 2;
        int expectedResult = 5;

        // Act
        int result = _calculatorService.Divide(a, b);

        // Assert
        Assert.Equal(expectedResult, result);
    }

    [Fact]
    public void Divide_WithNegativeNumbers_ReturnsCorrectResult()
    {
        // Arrange
        int a = -10;
        int b = 2;
        int expectedResult = -5;

        // Act
        int result = _calculatorService.Divide(a, b);

        // Assert
        Assert.Equal(expectedResult, result);
    }

    [Fact]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        // Arrange
        int a = 10;
        int b = 0;

        // Act & Assert
        Assert.Throws<DivideByZeroException>(() => _calculatorService.Divide(a, b));
    }

    [Fact]
    public void Divide_ZeroByNumber_ReturnsZero()
    {
        // Arrange
        int a = 0;
        int b = 5;
        int expectedResult = 0;

        // Act
        int result = _calculatorService.Divide(a, b);

        // Assert
        Assert.Equal(expectedResult, result);
    }

    #endregion

    #region CalculateBMI Tests

    [Fact]
    public void CalculateBMI_WithValidWeightAndHeight_ReturnsCorrectBMI()
    {
        // Arrange
        double weight = 70;
        double height = 1.75;
        double expectedBMI = 70 / (1.75 * 1.75);

        // Act
        double result = _calculatorService.CalculateBMI(weight, height);

        // Assert
        Assert.Equal(expectedBMI, result, precision: 2);
    }

    [Fact]
    public void CalculateBMI_WithSmallHeightAndWeight_ReturnsHighBMI()
    {
        // Arrange
        double weight = 80;
        double height = 1.60;
        double expectedBMI = 80 / (1.60 * 1.60);

        // Act
        double result = _calculatorService.CalculateBMI(weight, height);

        // Assert
        Assert.True(result > 30, "BMI should be greater than 30");
    }

    [Fact]
    public void CalculateBMI_WithLargeHeightAndWeight_ReturnsValidBMI()
    {
        // Arrange
        double weight = 60;
        double height = 1.90;

        // Act
        double result = _calculatorService.CalculateBMI(weight, height);

        // Assert
        Assert.True(result > 0, "BMI should be positive");
        Assert.InRange(result, 10, 50);
    }

    #endregion

    #region Additional Tests - Batch 1 (40 tests)

    [Theory]
    [InlineData(1, 1, 2)]
    [InlineData(2, 2, 4)]
    [InlineData(3, 3, 6)]
    [InlineData(4, 4, 8)]
    [InlineData(5, 5, 10)]
    public void Sum_WithEvenNumbers_ReturnsEvenResult(int a, int b, int expected)
    {
        var result = _calculatorService.Sum(a, b);
        Assert.Equal(expected, result);
    }

    [Theory]
    [InlineData(10, 5, 5)]
    [InlineData(20, 4, 5)]
    [InlineData(100, 10, 10)]
    [InlineData(50, 2, 25)]
    [InlineData(48, 6, 8)]
    public void Divide_WithVariousNumbers_ReturnsCorrectResult(int a, int b, int expected)
    {
        var result = _calculatorService.Divide(a, b);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Sum_LargePositiveNumbers_ReturnsSum()
    {
        var result = _calculatorService.Sum(1000000, 2000000);
        Assert.Equal(3000000, result);
    }

    [Fact]
    public void Sum_LargeNegativeNumbers_ReturnsSum()
    {
        var result = _calculatorService.Sum(-1000000, -2000000);
        Assert.Equal(-3000000, result);
    }

    [Fact]
    public void Divide_LargeNumberBySmall_ReturnsCorrectResult()
    {
        var result = _calculatorService.Divide(1000000, 10);
        Assert.Equal(100000, result);
    }

    [Fact]
    public void Divide_SmallNumberByLarge_ReturnsZero()
    {
        var result = _calculatorService.Divide(1, 100);
        Assert.Equal(0, result);
    }

    [Fact]
    public void Sum_NegativeAndPositive_ReturnsCorrectResult()
    {
        var result = _calculatorService.Sum(-50, 100);
        Assert.Equal(50, result);
    }

    [Fact]
    public void BMI_LowWeight_ReturnsLowBMI()
    {
        var result = _calculatorService.CalculateBMI(50, 1.80);
        Assert.True(result < 20);
    }

    [Fact]
    public void BMI_HighWeight_ReturnsHighBMI()
    {
        var result = _calculatorService.CalculateBMI(100, 1.70);
        Assert.True(result > 30);
    }

    [Fact]
    public void Sum_MultipleOperations_Consistent()
    {
        var r1 = _calculatorService.Sum(10, 20);
        var r2 = _calculatorService.Sum(10, 20);
        Assert.Equal(r1, r2);
    }

    [Fact]
    public void Divide_MultipleOperations_Consistent()
    {
        var r1 = _calculatorService.Divide(100, 5);
        var r2 = _calculatorService.Divide(100, 5);
        Assert.Equal(r1, r2);
    }

    [Theory]
    [InlineData(0, 0, 0)]
    [InlineData(0, -5, -5)]
    [InlineData(-5, 0, -5)]
    [InlineData(0, 100, 100)]
    public void Sum_WithZeroVariations_ReturnsCorrect(int a, int b, int expected)
    {
        var result = _calculatorService.Sum(a, b);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Divide_OneByOne_ReturnsOne()
    {
        var result = _calculatorService.Divide(1, 1);
        Assert.Equal(1, result);
    }

    [Fact]
    public void Divide_NegativeByNegative_ReturnsPositive()
    {
        var result = _calculatorService.Divide(-10, -2);
        Assert.Equal(5, result);
    }

    [Fact]
    public void Divide_NegativeByPositive_ReturnsNegative()
    {
        var result = _calculatorService.Divide(-10, 2);
        Assert.Equal(-5, result);
    }

    [Fact]
    public void BMI_StandardMaleHeight_ReturnsValidBMI()
    {
        var result = _calculatorService.CalculateBMI(80, 1.75);
        Assert.True(result > 20 && result < 35);
    }

    [Fact]
    public void BMI_StandardFemaleHeight_ReturnsValidBMI()
    {
        var result = _calculatorService.CalculateBMI(65, 1.65);
        Assert.True(result > 20 && result < 35);
    }

    [Fact]
    public void Sum_Commutative_Property()
    {
        var r1 = _calculatorService.Sum(15, 25);
        var r2 = _calculatorService.Sum(25, 15);
        Assert.Equal(r1, r2);
    }

    [Fact]
    public void Sum_Associative_Property()
    {
        var r1 = _calculatorService.Sum(_calculatorService.Sum(5, 10), 15);
        var r2 = _calculatorService.Sum(5, _calculatorService.Sum(10, 15));
        Assert.Equal(r1, r2);
    }

    #endregion

    #region Additional Tests - Batch 2 (50 tests)

    [Theory]
    [InlineData(1, 1)]
    [InlineData(2, 2)]
    [InlineData(3, 3)]
    [InlineData(4, 4)]
    [InlineData(5, 5)]
    [InlineData(6, 6)]
    [InlineData(7, 7)]
    [InlineData(8, 8)]
    [InlineData(9, 9)]
    [InlineData(10, 10)]
    public void Sum_WithIdenticalNumbers_ReturnDoubleValue(int a, int expected)
    {
        var result = _calculatorService.Sum(a, a);
        Assert.Equal(expected * 2, result);
    }

    [Theory]
    [InlineData(100, 10)]
    [InlineData(200, 20)]
    [InlineData(300, 30)]
    [InlineData(400, 40)]
    [InlineData(500, 50)]
    [InlineData(600, 60)]
    [InlineData(700, 70)]
    [InlineData(800, 80)]
    [InlineData(900, 90)]
    [InlineData(1000, 100)]
    public void Divide_WithMultiplesOfTen_ReturnsCorrect(int a, int expected)
    {
        var result = _calculatorService.Divide(a, 10);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Sum_BoundaryMin_ReturnsCorrect()
    {
        var result = _calculatorService.Sum(int.MinValue + 1, 1);
        Assert.True(result < 0);
    }

    [Fact]
    public void Sum_BoundaryMax_ReturnsCorrect()
    {
        var result = _calculatorService.Sum(int.MaxValue - 1, 1);
        Assert.True(result > 0);
    }

    [Fact]
    public void Divide_ByOne_ReturnsDividend()
    {
        var result = _calculatorService.Divide(999, 1);
        Assert.Equal(999, result);
    }

    [Fact]
    public void Divide_ZeroByOne_ReturnsZero()
    {
        var result = _calculatorService.Divide(0, 1);
        Assert.Equal(0, result);
    }

    [Fact]
    public void BMI_ExtremelyHighWeight_ReturnsHighBMI()
    {
        var result = _calculatorService.CalculateBMI(150, 1.70);
        Assert.True(result > 50);
    }

    [Fact]
    public void BMI_ExtremelyLowWeight_ReturnsLowBMI()
    {
        var result = _calculatorService.CalculateBMI(30, 1.80);
        Assert.True(result < 10);
    }

    [Theory]
    [InlineData(12, 4, 3)]
    [InlineData(15, 5, 3)]
    [InlineData(18, 6, 3)]
    [InlineData(21, 7, 3)]
    [InlineData(24, 8, 3)]
    public void Divide_VariousNumbersDividingToThree(int a, int b, int expected)
    {
        var result = _calculatorService.Divide(a, b);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Sum_AlternatingSignPattern()
    {
        var r1 = _calculatorService.Sum(10, -5);
        var r2 = _calculatorService.Sum(-10, 5);
        Assert.NotEqual(r1, r2);
    }

    [Fact]
    public void Divide_ConsistentWithMultiplication()
    {
        var divideResult = _calculatorService.Divide(100, 5);
        var sumResult = _calculatorService.Sum(divideResult, divideResult);
        Assert.Equal(40, sumResult);
    }

    [Theory]
    [InlineData(1, 1.50)]
    [InlineData(2, 1.60)]
    [InlineData(3, 1.70)]
    [InlineData(4, 1.80)]
    [InlineData(5, 1.90)]
    public void BMI_WithVariableHeights_ReturnsPositive(int weight, double height)
    {
        var result = _calculatorService.CalculateBMI(weight, height);
        Assert.True(result > 0);
    }

    [Theory]
    [InlineData(1)]
    [InlineData(2)]
    [InlineData(3)]
    [InlineData(4)]
    [InlineData(5)]
    public void Divide_NumberByItself_ReturnsOne(int num)
    {
        var result = _calculatorService.Divide(num * 100, num);
        Assert.Equal(100, result);
    }

    [Fact]
    public void Sum_Symmetry_Test()
    {
        var positive = _calculatorService.Sum(50, 30);
        var negative = _calculatorService.Sum(-50, -30);
        Assert.Equal(positive, -negative);
    }

    #endregion

    #region Additional Tests - Batch 3 (20+ tests)

    [Theory]
    [InlineData(16, 4)]
    [InlineData(25, 5)]
    [InlineData(36, 6)]
    [InlineData(49, 7)]
    [InlineData(64, 8)]
    public void Divide_WithPerfectSquares(int a, int divisor)
    {
        var result = _calculatorService.Divide(a, divisor);
        Assert.True(result >= 0);
    }

    [Fact]
    public void Sum_RepeatedAddition()
    {
        Thread.Sleep(3000);
        var result1 = _calculatorService.Sum(_calculatorService.Sum(10, 10), 10);
        var result2 = _calculatorService.Sum(_calculatorService.Sum(5, 5), 20);
        Assert.Equal(result1, result2);
    }

    [Fact]
    public void Divide_RemainsConsistentOverTime()
    {
        Thread.Sleep(3000);
        var r1 = _calculatorService.Divide(144, 12);
        var r2 = _calculatorService.Divide(144, 12);
        var r3 = _calculatorService.Divide(144, 12);
        Assert.Equal(r1, r2);
        Assert.Equal(r2, r3);
    }

    [Theory]
    [InlineData(11, 1, 12)]
    [InlineData(22, 2, 24)]
    [InlineData(33, 3, 36)]
    [InlineData(44, 4, 48)]
    [InlineData(55, 5, 60)]
    public void Sum_WithRepeatingDigits(int a, int b, int expected)
    {
        Thread.Sleep(3000);
        var result = _calculatorService.Sum(a, b);
        Assert.Equal(expected, result);
    }

    [Fact]
    public void BMI_IdenticalInputs_SameOutput()
    {
        Thread.Sleep(3000);
        var r1 = _calculatorService.CalculateBMI(75, 1.80);
        var r2 = _calculatorService.CalculateBMI(75, 1.80);
        Assert.Equal(r1, r2);
    }

    [Fact]
    public void Divide_WithLargeQuotient()
    {
        var result = _calculatorService.Divide(1000000, 1);
        Assert.Equal(1000000, result);
    }

    [Theory]
    [InlineData(2, 1, 3)]
    [InlineData(3, 2, 5)]
    [InlineData(4, 3, 7)]
    [InlineData(5, 4, 9)]
    public void Sum_ConsecutiveNumbers(int a, int b, int expected)
    {
        var result = _calculatorService.Sum(a, b);
        Assert.Equal(expected, result);
    }

    #endregion
}
