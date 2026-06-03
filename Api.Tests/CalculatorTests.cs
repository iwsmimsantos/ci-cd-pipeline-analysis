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
}
