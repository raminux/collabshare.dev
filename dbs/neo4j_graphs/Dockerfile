FROM neo4j:latest

# Set the Neo4j password
# ENV NEO4J_AUTH=none
ENV NEO4J_AUTH=neo4j/mypass123

# Copy any custom configuration files
COPY neo4j.conf /var/lib/neo4j/conf/

# Set the working directory to the Neo4j data directory
WORKDIR /data

# Expose the Neo4j ports
EXPOSE 7474 7473 7687

# Start Neo4j
CMD ["neo4j"]
