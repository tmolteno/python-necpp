template<typename T>
class safe_array
{
public:
  T* data() const;
  T& getItem(int64_t i);
};
%extend safe_array<nec_float> {

  nec_float& getItem(int64_t i) {
        return $self->getItem(i);
    }
}
  
