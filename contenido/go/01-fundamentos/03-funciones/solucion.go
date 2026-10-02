package ejercicio

func MinMax(nums ...int) (min, max int, ok bool) {
	if len(nums) == 0 {
		return 0, 0, false
	}
	min, max = nums[0], nums[0]
	for _, n := range nums[1:] {
		if n < min {
			min = n
		}
		if n > max {
			max = n
		}
	}
	return min, max, true
}

func Map(xs []int, f func(int) int) []int {
	res := make([]int, len(xs))
	for i, x := range xs {
		res[i] = f(x)
	}
	return res
}

func NuevoContador(desde int) func() int {
	siguiente := desde
	return func() int {
		actual := siguiente
		siguiente++
		return actual
	}
}

func Componer(f, g func(int) int) func(int) int {
	return func(x int) int { return f(g(x)) }
}
