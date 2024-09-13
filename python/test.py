def fact(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n < 0:
        raise ValueError("n must be positive")
    return n * fact(n-1)

def main():
    print(fact(3))


if __name__ == "__main__":
    main()