# TwitchAPI

A wrapper for the [twitch.tv API](https://dev.twitch.tv/docs/) written in Python. The API they provide is web based, however this version will allow for easy access in Python.

You must import the class provided in the `TwitchPy.py` file, and then you can access the API by creating a new TwitchPy class, `api = TwitchPy("YOUR API KEY HERE")`.

Many operations require a users OAuth key, for this you must add they OAuth key with `api.setAuthToken("CLIENTS AUTH TOKEN HERE")`. I plan to, in future, add authentication to the API but this is just a first draft.

The current version is *v0.1.0* and you can check which version you have with the output from `TwitchPy.version()`