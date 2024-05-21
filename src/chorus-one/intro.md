# How Chorus One Operates Nodes

At Chorus One we operate nodes reliably for more than 50 networks.
Over time we’ve noticed patterns across those networks,
and we learned what approaches work well.
Years of incident response have forced us
to build our infrastructure in a way that is resilient.
In this section of the book,
we describe the infrastructure that we have converged on.

In short,
we run our workloads primarily on bare metal machines
in data centers operated by multiple different providers,
in many different countries.
This gives us maximum performance and resiliency at a cost-effective price.
This approach is not without challenges:
engineering is about making trade-offs.
In each of the following chapters we highlight one aspect of our setup,
and why it works the way it does.
