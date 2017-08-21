template<typename T>
class safe_array {
public:
  T& getItem(int64_t i);
};

template<typename T>
class safe_matrix {
public:
  T& getItem(int32_t i, int32_t j);
  int32_t rows();
  int32_t cols();
};