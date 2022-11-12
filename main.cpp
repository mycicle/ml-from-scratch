#include <iostream>
#include <sstream>

template <typename T> class MatrixBase {
    // every matrix base must implement data storage as a 1D array
    /*
     * dot(m1, m2) returns new T
     * m1.multiply(m2) inplace multiplication changes m1
     * multiply(m1, m2) returns new Matrix // equivalent to m1 * m2
     *
     * m1.add(m2) inplace addition changes m1
     * add(m1, m2) returns new Matrix // equivalent to m1 + m2
     *
     * m1.subtract(m2) inplace subtraction changes m1
     * subtract(m1, m2) // equivalent to m1 + m2
     */
protected:
    T *data;
public:
    explicit MatrixBase() : data(nullptr) {}

    MatrixBase(const T* input): data(nullptr) {
        if (input) {
            data = new T[std::size(input)];
            memcpy(data, input, std::size(input));
        }
    }

    MatrixBase(const MatrixBase<T>& other): data(nullptr) {
        MatrixBase(other.data);
    }

    ~MatrixBase() {
            delete[] data;
    }

    MatrixBase(MatrixBase<T>&& other) noexcept {
        std::swap(other.data, data);

        return *this;
    }

    MatrixBase<T>& operator =(const MatrixBase<T>& other) {
        return *this = MatrixBase(other);
    }

    MatrixBase<T>& operator =(MatrixBase<T>&& other) {
        std::swap(this->data, other.data);

        return *this;
    }

    T* getData() {
        return data;
    }
    /*
     * Dot Product
     */
    // T _ = dot(mat1, mat2);
    friend T dot(const MatrixBase<T>& left, const MatrixBase<T>& right ) {
        if (!left.validate(right)) {
            throw std::invalid_argument("validate failed on dot product");
        }
        T answer = 0;
        for (int i = 0; i < left._size; i++) {
            answer += (left.data[i] * right.data[i]);
        }

        return answer;
    }

    /*
     * Matrix Multiplication
     * Implementation left to the child classes
     */
    virtual MatrixBase<T>& operator *(const MatrixBase<T>& other) const {}
    virtual void multiply(const MatrixBase<T>& other) {}
    friend MatrixBase<T>& multiply(const MatrixBase<T>& left, const MatrixBase<T>& right) {
        return left * right;
    }

    /*
     * Matrix Addition
     */
    // MatrixBase mat = mat1 + mat2
    MatrixBase<T>& operator +(const MatrixBase<T>& other) const {
        if (!validate(other)) {
            throw std::invalid_argument("validate check failed on addition");
        }

        T* output = new T[other._size];
        for (int i = 0; i < other._size; i++) {
            output[i] = data[i] + other.data[i];
        }

        return new MatrixBase<T>(_size, output);
    }
    // mat1.add(mat2)
    void add(const MatrixBase<T>& other) {}
    // MatrixBase mat = add(mat1, mat2)
    friend MatrixBase& add(const MatrixBase<T>& left, const MatrixBase<T>& right) {
        return left + right;
    }

    /*
     * Matrix Subtraction
     */
    // MatrixBase mat = mat1 - mat2
    MatrixBase<T> operator -(const MatrixBase<T>& other) const {
        if (!validate(other)) {
            throw std::invalid_argument("validate check failed on subtraction");
        }

        T* output = new T[other._size];
        for(int i = 0; i < other._size; i++) {
            output[i] = data[i] - other.data[i];
        }

        return MatrixBase<T>(_size, output);
    }
    // mat1.subtract(mat2)
    void subtract(const MatrixBase<T>& other) {}
    // MatrixBase mat = subtract(mat1, mat2)
    friend MatrixBase& subtract(const MatrixBase<T>& left, const MatrixBase<T>& right) {
        return left - right;
    }

    [[nodiscard]] bool validateData(const MatrixBase<T>& other) const {
        if (!data) return false;

        if (!other.data) return false;

        return true;
    }
    [[nodiscard]] bool validateSize(const MatrixBase<T>& other) const {
        if (_size != other._size) return false;

        return true;
    }
    [[nodiscard]] bool validate(const MatrixBase<T>& other) const {
        return validateSize(other) && validateData(other);
    }

    friend std::ostream& operator <<(std::ostream& s, const MatrixBase<T>& m ) {
        std::stringstream ss;
        for (int i = 0; i < m._size; i++) {
            ss << m.data[i] << ", ";
        }
        ss << "\n";

        return s << ss.str();
    }
};


int main() {
    std::cout << "Hello, World!" << std::endl;
    MatrixBase<int> m1(100, new int[100]{5});
    MatrixBase<int> m2(100, new int[100]{10});
    MatrixBase<int> m3 = m1 - m2;
    int* data = m3.getData();
    for (int i = 0; i < 100; i++) {
        std::cout << data[i] << " " << std::endl;
    }

    std::cout << m3 << std::endl;
    return 0;
}
