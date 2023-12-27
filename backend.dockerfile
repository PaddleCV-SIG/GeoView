FROM paddlepaddle/paddle:2.4.1
RUN wget https://github.com/girder/large_image_wheels/raw/wheelhouse/GDAL-3.4.1-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
#COPY GDAL-3.4.1-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl .
RUN pip install GDAL-3.4.1-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
RUN rm -rf GDAL-3.4.1-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
RUN mkdir /app
COPY PaddleRS /app/PaddleRS
WORKDIR /app/PaddleRS
RUN pip install -r /app/PaddleRS/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -e .
COPY backend /app/backend
WORKDIR /app/backend
RUN pip install -r /app/backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENTRYPOINT ["python", "app.py"]