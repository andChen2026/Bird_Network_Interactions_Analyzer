### Overview
A more specific field in Social Network Analysis, in which birds are depicted using nodes and connections using edges or arcs. The connections may be directed or undirected, and several metrics are used to analyze the socio-gram.

Centrality is a set of quantitative measures the importance of any given bird.
- Betweenness - Identifies the actor that is present along most shortest paths among all other actors
	- $G(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$
	- $W(v) = argmax_v(G(v))$
	- $\sigma_{st}$ represents the shortest path from s to t
	- $\sigma_{st}(v)$ represents the shortest path from s to t containing v
- Which bird is the bottleneck between all other birds? Disease, communication, etc.

- Closeness - Identifies the bird that can reach all others with the least average steps
	- $N(v) = \sum_{t \neq v}^{T} S(v, t)$
	- $D(v) = \sum_{t \neq v} ^ {T} P(v, t)$
	- $T(v) = N(v)/D(v)$
	- $G(v) = \frac{1}{T(v)}$
	- $W(v) = argmin_v(G(v))$

	- $N(v)$ measures the number of steps from $v$ to $t$, length of path
	- $D(v)$ measures if there is a path from $v$ to $t$, $1$ for yes and $0$ for no
	- $T(v)$ measures the average steps from $v$ to $t$
	- $G(v)$ measures the reciprocal of $T(v)$, larger is better
	- $W(v)$ measures the minimum $G(v)$ for a $v$, the best node $v$
- Which bird is able to reach other birds using the least average steps?

- Degree - Identifies the bird with the highest connectivity
	- $W(v) = argmax_v(\sum_{t \neq v} Out(t, v) + In(v, t))$
- Which bird is most connected to other birds?
### Implementation
A Graph data structure is utilized, implemented using a directed adjacency list. The intuition is that a bird song may be heard by other birds, which may not all sing back. Since the initial data set is small, an adjacency list - Linked List will yield a much smaller memory footprint than an adjacency matrix. 

A massive memory bottleneck will be event propagation. If bird A sings, it may affect up to K birds in the entire network model. To reduce this burden, a single event object will be created, and a pointer reference will be passed to each of the other bird objects.

An important note to make is that the greater the degree of the bird, the more likely it will be invoked and an action to be performed. Thus, we will use this heuristic in our implementation. We will rank the birds by their degree metric and cache those that are more likely to be invoked. For those that have low degrees, we will fetch them from memory. This scheme reduces the average memory fetch time, which should realize speed gains. Caveat: if the graph is incredibly dense (connectivity is nearly 1), then no memory and speed gains will be realized.

The Network Graph will be based on the physical location of the bird, with each site having its own. Individual bird recordings will grouped together as one Node based on proximity. Afterwards, interactions among individual birds will be processed and analyzed using network based algorithms.

