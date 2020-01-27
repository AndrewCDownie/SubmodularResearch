syms x1;
syms x2;
syms x3;
syms x4;

syms d12;
syms d13;
syms d23;
syms d14;
syms d24;
syms d34;


D = [0,d12,d13,d14;d12,0,d23,d24;d13,d23,0,d34;d14,d24,d34,0]
X = [x1,x2,x3,x4]

delt(X,D,3,[])

f1 = f(X,D,[1,2,3])
f2 = f(X,D,[2,1,3])
f3 = f(X,D,[3,2,1])

f1
f2
f3
f4 = f(X,D,[1,2,3,4])

f5 = f(X,D,[2,1,3,4])
f6 = f(X,D,[3,2,1,4])
f7 = f(X,D,[4,2,1,3])
f4
f5
f6
f7


function fn = f(X,D,S)
	[m,n] = size(S)
	fn = 0
	for i = 1:n
		S_i = []
		for j = 1:i-1
			S_i = [S_i S(j)]
		end
		fn= fn + delt(X,D,S(i),S_i)
	end
end


function delta = delt(X,D,i,S)
	delta = X(i)
	[m,n] = size(S)
	for j = 1:n
		disp(j)
		delta = delta + D(i,S(j))*X(S(j))
	end	

end

