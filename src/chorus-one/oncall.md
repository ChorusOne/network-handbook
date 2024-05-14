# Oncall rotation

In [the previous chapter](monitoring-and-alerting.md)
we looked at how we monitor our nodes
and generate alerts when anything is amiss.
Our 24/7 oncall rotation is standing by
to be able to handle those alerts within minutes.

### Team

The majority of our engineering team consists of what we call _platform engineers_.
Some companies call this role _site reliability engineering_ instead.
Platform engineers are repsponsible for our infrastructure,
operating our chains,
and periodically,
for handling alerts.

Chorus One is a remote company and our team spans a wide range of time zones,
from Asia to the Americas.
The majority of our people are located in Europe.

### Coverage

We ensure that at least one engineer is able to handle alerts all times.
We employ enough people that we can guarantee this;
in case of unforeseen personal events we can find somebody else to step in.
A shift is at least a full day,
we do not use a follow-the-sun schedule.
If an alert fires outside of regular working hours,
an oncall engineer gets paged.
That might be at night.

### Preventive measures

Our oncall rotation enables us to respond to emergencies 24/7,
but of course engineers still prefer a quiet night of sleep.
The best incident response is not having an incident in the first place.
Internally we achieve that [through redundancy](reliable-systems.md).
For network-wide incidents,
the second half of this book contains our recommendations to node software authors
to minimize the risk of outages.
[The timing section of the release engineering chapter](../node-software/release-engineering.md#timing)
is particularly relevant.
