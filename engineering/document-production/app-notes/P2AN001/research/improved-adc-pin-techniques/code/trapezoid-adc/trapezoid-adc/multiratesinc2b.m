
t=1:120;
d=t*0;

for m=5:110 % inpulse position

inputbits=(t==m);
%inputbits=t*0+1;


s1=cumsum(inputbits);
s2=cumsum(s1);

%d(m)=(s2(100)-s2(90))-(s2(20)-s2(10));
d(m)= s2(100) -s2(90) -s2(20) +s2(10); % same as above

%d(m)=(s2(100)-s2(90))-(s2(20)-s2(15))*2; %example asymmetric filter
%d(m)= s2(100) - 2*s2(95) +s2(90) -s2(20) +2*s2(15) -s2(10); 
%d(m)= 1*s2(100) - 2*s2(95) +1*s2(90) -1*s2(20) +2*s2(15) -1*s2(10);
 % emulated sinc3 shape
%d(m)= s2(100) + s2(95) +s2(90) -s2(85) -s2(80) -s2(75)            -s2(35)  - s2(30) -s2(25) +s2(20) +s2(15) +s2(10) ;
%d(m)= s2(100) + s2(95) +s2(90) + s2(85) -s2(80) -s2(75) -s2(70) -s2(65)          -s2(45) - s2(40) -s2(35) - s2(30) +s2(25) +s2(20) +s2(15) +s2(10) ;

end

stem(d)
title("s2(100) -s2(90) -s2(20) +s2(10)")
