# Choose your desired base image
FROM jupyter/scipy-notebook:82b978b3ceeb


MAINTAINER Jupyter Project <jupyter@googlegroups.com>


# Install Python 2 Tensorflow
RUN conda install --quiet --yes -n python2 'tensorflow=1.0.1'