## dependency.pdf

The current file dependencies and proposed separations

- as a package, we need to decide bycon's public functions.
- cytoband_utils.py is categorized to byconeer.
- still not sure about where we should put service.py.


## architecture.pdf

Some thoughts about the general structure

- bycon is a bit too heavy as a combination of the beacon and the GA4GH data model, we may consider to separate them more clearly.
- I think pgy and other future applications want to reuse the data model part of bycon, not the beacon spec.
- bycon also contains some common utility functions, we may also consider moving them out.
- all modules make direct operations on the database, we can probably combine the utils and a db class to provide centralized access.
- the "alternative architecture" is not a very mature idea, just some general thoughts.
- we may consider separate bycon as the beacon specification (most of the current byconcore) and the data model (most of the current byconeer).
- we could work towards a more layered structure to replace the current mixture.

