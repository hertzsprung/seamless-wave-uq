using Test

@testset "single timestep" begin
	h = 1
	q = 2

	N = 4
	u = zeros((2, 2, N))

	u[h,1,:] .= 5.0
	u[h,2,:] .= 1.0

	println("h_0 ", u[h,1,:])
	println("h_1 ", u[h,2,:])

	println("q_0 ", u[q,1,:])
	println("q_1 ", u[q,2,:])
end;
