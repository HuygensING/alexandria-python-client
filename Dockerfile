FROM jupyter/datascience-notebook
ENV wd=/data
ADD . ${wd}
WORKDIR ${wd}
RUN pip install pydot
