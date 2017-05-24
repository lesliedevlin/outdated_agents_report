# server_count_percentages
CloudPassage Halo Server Count Percentages report

Disclaimer: This script is provided as is. USE AT YOUR OWN RISK.
NOT A SUPPORTED SOLUTION

# Configure
To configure script add API Key information to cloudpassage.yml File
>key_id: your_api_key_id
>secret_key: your_api_secret_key

In cloudpassage.yml, set root_group_id to the group ID of your top-level group.
This ID is a 32-character string that will appear in your URL after you log in, e.g.:

https://portal.cloudpassage.com/halo/environment/group/<group-ID>/summary

# Requirements

This script requires Python 2.7.10 or greater
This script requires the CloudPassage Python SDK
> pip install cloudpassage

This script requires the Requests Python module.
>pip install requests

Install from pip with pip install cloudpassage. If you want to make modification
s to the SDK you can install it in editable mode by downloading the source from 
this github repo, navigating to the top directory within the archive and running
 pip install -e . (note the . at the end). Or you can visit https://github.com/c
loudpassage/cloudpassage-halo-python-sdk to clone it directly from our github.


# Running

Run python server_count_percentages.py to generate a single .csv report of your organization's agent usage at the time you run the script. This script assumes that groups immediately below the root group represent business units and reports on the agent usage as a percentage of total account usage.  This can be used for estimating billbacks as well as general account usage auditing.



# License

Copyright (c) 2017, CloudPassage, Inc. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 
* Neither the name of the CloudPassage, Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CLOUDPASSAGE, INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED ANDON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
