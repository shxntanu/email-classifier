<div align="center">
    <img src="assets/Repo Cover.png" />
</div>

> This project was the **winner** at **Barclays Pune** and bagged the **3rd Prize** 🏆 overall at [Barclays Hack-O-Hire 2024](https://www.hackerearth.com/challenges/hackathon/hack-o-hire/)

Receiving hundreds or thousands of mails a day and then figuring out which mail should be directed to which person can be a daunting task. This project aims to tackle that problem. We created a solution that can effectively classify emails based on not only their content, but also the context in which they are written, and then route them to the respective department(s) or person(s) in charge.

## Our Team

- [Anish Pawar](https://github.com/anishpawarrr)
- [Mihir Deshpande](https://github.com/mihirdesh)
- [Piyush Agarwal](https://github.com/piyushhagarwal)
- [Shantanu Wable](https://github.com/shxntanu)

## Problem Statement

### Email classification based on the content

Multiple emails from customers/clients that are dealt with different teams based on the context. This solution should enable auto-classification of emails based on the context, so the same can be routed to best suited team for further processing.

### Technology

- Python
- Anaconda platform

### Other Considerations

The data selected should represent sufficient variation to be able to demonstrate classification clearly. Expectation from participants will be to present overall solution with clear focus on characteristics of data and holistic nature of the implementation.
Data

For solving this problem, participants can decide to leverage data available on public forums like Kaggle (preferably from finance domain). But the model should be easy to configure/retrain for similar topics.

### Design Considerations

This model should be easy to deploy to execute either as batch or real time.

Focus should also be on making it efficient from resource consumption standpoint and something that can be hosted as containers.

### Benefits

Auto-email classification will enable significant reduction in manual efforts

## Solution

<div align="center">
    <img src="assets/EC Flow Diagram.png" />
    <br />

_Process Flow Diagram_
    
</div>

Our solution works as follows:

1. **Email Receiving**: We have a root node, which acts as the central email receiver in an organization. It is continuously monitored for new emails through the IMAP protocol (which is done in a continuously running python service). It can be any professional email service like Gmail, Outlook, etc.
2. **Distributed Task Queue**: Each email is then sent to a distributed task queue, where it is processed by multiple parallel workers, thus ensuring that the system is scalable and can handle a large number of emails. The system can thus **scale horizontally** very effectively.
3. **Parsing**: The email is parsed and the content is extracted (including attachments!)
4. **Encryption**: The content is encrypted using a powerful cypher.
5. **Sending to Server**: The encrypted content is sent to the server where it is decrypted.
6. **Large Language Model**: The content is passed to our powerful Large Language Model, Mixtal 8x7b which extracts the meaning, context and the sentiment from the email and determines the department/team to which the email should be routed to, including any CCs or BCCs that it deems important.
7. **Summarization**: The email is then summarized by a lighter model, and the summary is sent back to the service.
8. **Message Composition**: The service then composes a new email with the summary (for quick reference) and the sentiment (e.g. Urgent, Complaint, Neutral) and the original email (along with attachments), and sends it back to the root node.
9. **Routing**: The full email is then routed to the respective department/team/person through the SMTP Protocol.
10. **Feedback System**: The system also has a feedback system, where in the case of incorrect routing, the user can provide feedback, which is then used to retrain the model.
