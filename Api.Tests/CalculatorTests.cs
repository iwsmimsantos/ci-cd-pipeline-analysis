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
}
