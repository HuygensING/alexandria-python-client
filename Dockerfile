FROM jupyter/datascience-notebook
# user is set to jovyan

ENV vol=$HOME/work
VOLUME ${vol}
COPY example.ipynb  ${vol}/
#RUN chown jovyan ${vol}/*

ENV wd=/tmp
ADD . ${wd}
WORKDIR ${wd}
RUN pip install --user pydot
RUN python setup.py install --user
WORKDIR ${vol}