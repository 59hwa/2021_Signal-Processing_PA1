sample = double(rgb2gray(imread('start.jpg')));
data = zeros(360,480,10);
for i = [1:10]
    data(:,:,i) = double(rgb2gray(imread(['0' num2str(i*10,'%03d') '.jpg'])));
end
deltax = 30;
deltay = 27;
xpath = 275;
ypath = 137;
samplei = sample(ypath:ypath+deltay-1,xpath:xpath+deltax-1);
Mata= Fmat(deltay);
Matb= Fmat(deltax);
samplef = Fourier(Mata,Matb,samplei);
for z = 1:10
    datai = data(:,:,z);
    k = zeros(360-deltay,480-deltax);
    for x = 1:480-deltax
        for y = 1:360-deltay
            k(y,x) = Corr(Mata,Matb,samplef,datai(y:y+deltay-1,x:x+deltax-1));
        end
    end
    [j1, i1] = find(k == max(max(k)));[j1,i1]
    saveas(imagesc(k),['Activaion_Map_' '0' num2str(z*10,'%03d') '.jpg']);
    img = imread(['0' num2str(z*10,'%03d') '.jpg']);
    f = figure;
    imshow( img, 'border', 'tight' ); 
    hold on;
    rectangle('Position', [i1 j1 deltax deltay] );
    frm = getframe(f);
    imwrite( frm.cdata, ['result' '0' num2str(z*10,'%03d') '.jpg'] );
    hold off;
end

function f = Fourier(Mata, Matb, n)
    f = Mata*n*Matb;
end
function f = InFourier(Mata, Matb, n)
    k = size(n);
    f = conj(Mata)*n*conj(Matb)./k(1,1)./k(1,2);
end
function f = Fmat(n)
    for k = 1:n
        for j = 1:n
            f(k,j) = exp(-2*pi*i/n*(k-1)*(j-1));
        end
    end
end
function f= Corr(Mata, Matb, samplef, data)
    ma = samplef.*conj(Fourier(Mata, Matb, data));
    R = ma./abs(ma);
    r = InFourier(Mata, Matb, R);
    f = max(max(real(r))); %실수부를 반환
    %f = max(max(abs(r))); %절댓값을 반환
end

