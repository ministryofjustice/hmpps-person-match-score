# 3. Make Person Match Score Full Service

Date: 2024-12-06

## Status

Accepted

## Context

To facilitate the extension of the Splink Model to support matching for Core Person Record it is necessary to have access to data held within CPR.  A number of options to allow for this change have been considered.

### Move hmpps-person-match-score logic to hmpps-person-record
This would involve adding the ability to call python splink code within the core person record kotlin service.  It would likely involve a number of 'call outs' from Kotlin to Python

**Pros**
1. Single Project for core Core Person Record Team

**Cons**
1. More complex build pipeline and test infrastructure to test a combination of Kotlin, SQL and Python Code
2. Difficulties in monitoring, maintaining and releasing multiple code bases
3. Tight Coupling between CPR Services and Splink

### Give Direct Access to CPR DB from hmpps-person-match-score
**Pros**
1. Allows Splink access to all the data that it needs
2. Runs of a standard approach taken by data science to run tools on databases

**Cons**
1. Provides Tight Coupling between match score and person record
2. Creates Security Issues due to it having full access to all CPR data including Protected Characteristics

### Extend this service to be a fully fledged python service
This will mean the service will 
1. Have its own data store holding the minimal amount of data needed for scoring purposes
2. Listen to events 'fired' by hmpps-person-record in order to keep it's own data in store
3. Can optionally have a duck db instance embedded within Python

**Pros**
1. Gives hmpps-person-match-score the ability to store all local data needed for linking,  generating term frequency tables and carrying out Model Retraining
2. Creates a clean separation between business logic of core person and scoring / matching logic of splink

**Cons**
1. Python is not a standard hmpps tech stack.  So will require Core Person to ensure it always has a developer available that is capable of maintaining the project.
2. Additional security constraints as the service will no longer be stateless and will own data in it's own right.

## Decision
It has been decided to extend this service to be a fully fledged python service

## Consequences

This will ensure that all splink capabilities will be provided for by this project.  It will have its own pipeline,  tests and security implementations.