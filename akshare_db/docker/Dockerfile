# Use the official MongoDB image as the base image
FROM mongo:latest

# Install wget and other necessary tools
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean

# Install Miniconda
ENV PATH="/opt/conda/bin:${PATH}"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Create a virtual environment in Anaconda
RUN conda create -n myenv python=3.8

# Activate the virtual environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Install any additional packages you may need for your project
# For example, you can install pandas, numpy, etc.
RUN conda install -y pandas numpy

# Switch back to the default shell
SHELL ["/bin/bash", "-c"]

# Expose MongoDB port
EXPOSE 27017

# Start MongoDB service
CMD ["mongod"]

# You can add additional commands or configurations as needed