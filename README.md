# numberstation
A python script that simulates a number station. Has the ability to encrypt, decrypt and create a corresponding sound file (.wav).

## General

A number station is a station that transmits encrypted messages in number form. The message can contain any combination of letters, both upper and lower case, numbers, spaces and dots. The code can be modified for other language support, as well as more punctuation marks. The numbers are transmitted in groups of six.


## Script
The plaintext is encrypted using a random one time pad, of equal length as the message. A one time pad is cryptographically uncrackable, unless the generated key is either leaked or reused - in part or whole.
The randomness must be uniformly distributed and non-algorithmic, meaning that pythonic randomness (either from the modules rand or secrets) not enough. 

As a workaround random.org's API was used. As per the website, truly random numbers based on atmospheric noise are generated. Of course, it isn't wise trusting an external website for real-life applications. A suitable replacement would be either a dedicated hardware random generator or a homebrerw solution. An example of the latter would be using an RTL SDR dongle using RF noise to generate bits.<sup>[[1]](#one)</sup>

The API calls are carried out using the module requests.<sup>[[2]](#two)</sup>

The audio is generated using the module pydub.<sup>[[3]](#three)</sup> The module can manipulate .wav files, making the creation of the final file trivial. The audio message is structured as:

intro *2, (padcode *n, break,) number message *n, intro *2,

where padcode (optional) is for specifying which one time pad is used for the decryption, n is the number of repetitions, maximum 3.

The sounds used for intro and break can be changed by changing the corresponding file.

A very basic GUI, using tkinter, is provided.


## Resources, Modules

1. <a name="one"></a>[RTL-SDR true RNG](https://pthree.org/2015/06/16/hardware-rng-through-an-rtl-sdr-dongle/) 
2. <a name="two"></a>[Requests](https://github.com/psf/requests)
3. <a name="three"></a>[pydub](https://github.com/jiaaro/pydub)
4. [Male voice](https://soundbible.com/2008-0-9-Male-Vocalized.html)
5. [Folder Icon](https://www.shareicon.net/folder-open-file-button-interface-690535)






