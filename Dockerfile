FROM pbuterba/docker-lab:latest
RUN echo "Building Docker lab container!"
WORKDIR /home/data
CMD ["python3", "scripts.py"]