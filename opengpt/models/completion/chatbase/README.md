# ChatBase

ChatBase is a service offering chatgpt integration for websites for both gpt3.5-turbo and gpt-4.

[How to Use](https://github.com/uesleibros/OpenGPT/tree/main/opengpt/chatbase/DOC.md)

## Problems

Unfortunately it's slow, but that's because it doesn't use `text/event-stream`. Which is a type used to send already processed chunks of content to the client, instead it gets everything and then sends it all at once. So if you order something big it might take a while to ship.
