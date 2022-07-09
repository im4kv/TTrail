<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/im4kv/TTrail/main/images/logo-light.png">
    <img alt="TTrail" src="https://raw.githubusercontent.com/im4kv/TTrail/main/images/logo-dark.png">
  </picture>

  <h3 align="center">TTrail: AWS Cloudtrail Event History Analyzer</h3>

  <p align="center">
    Dynamically group events into a Tree-view style to easily understand what's happened in your environemnt
    <br />
    <br />
    <a href="https://github.com/im4kv/TTrail/issues">Report Bug</a>
    ·
    <a href="https://github.com/im4kv/TTrail/issues">Request Feature</a>
  </p>
</div>

[![TTrail Screen Shot][ttrail-screenshot]](https://github.com/im4kv/TTrail)


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

Most of the SME organizations rely on using default AWS Cloudtrail event history to check what's happend on their account (In the absese on AWS Config and Athena). In that cases you are dealing with tens of pages of events to check and filter.TTrail is designed for analyzing short timeframe events (e.g: last 30 minutes, past 8 hour, last day) and dynamically grouping them by service, action, etc so you could group thousands of events into couple of lines in an understadable treeview.


Here's why it suits you well:
* A service just broke an hour ago and you don't know where to start and what to filter?
* You have a security incident and you want to quickly understand who did what?
* You didn't setup and monitor your Cloudtrail events via another mechanism e.g Athena, Security Hub, Config, etc.
* your environemt consist of many service-account that may generate repetetive  events that makes filtering and page navigation a bit difficult. 
* You seek an start point to find what to jump in and analyze in detail

Of course, it is not here to replace your existing bulk event analysis tools and it is the early release of it. So I'll be adding more interesting features in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. 


<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

To get a TTrail up and running locally, follow these simple steps.

### Prerequisites

`TTrail` is using AWS [Boto3](https://aws.amazon.com/sdk-for-python/) library for it's connection to AWS Cloudtrail. if you already setup [AWS profiles](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/keys-profiles-credentials.html) (Access ID/Keys, Role Name and Profiles) using AWS CLI then you are good to go. otherwise <strong>it is required to [configure your AWS profile](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/keys-profiles-credentials.html). </strong> 

In case you have more than one AWS profile, you can select different profiles while running  `TTrail`.



### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

  ```sh
  python3 -m pip install ttrail 
  ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

  ```sh
  > ttrail --help  
  Options:
    --start-time TEXT      search start date, examples: "July 4, 2021 PST" , "21
                          July 2013 10:15 pm +0500" or human readables "1 hour
                          ago", "in 2 days". Defaults to "1 hour ago".
    --end-time TEXT        search end date, examples: "July 4, 2021 PST" , "21
                          July 2013 10:15 pm +0500" or human readables "1 hour
                          ago", "now". Defaults to "now".
    --profile TEXT         AWS Profile name to use. it will use "default" if
                          nothing else is specified.
    --skip-service-events  A Display filter to skip events with the user
                          identity of AWS service.
    --help                 Show this message and exit. 
  ```


TTrail comes with few options which are imporant to know. as an starting point you may want to select events for past one hour/day. to do so you should specify `--start-time` option. as the help says it accepts human readable times like 'one day ago' and it will transform it to what it needs to be. `--end-time` is also important that specify the end of search period and by default is set to current time and it is not mandatory. 

So here is an example of running TTrail to search for Cloudtrail events for last six hours.

  ```sh
  ttrail --start-time '6 hours ago'
  ```
  It is important to know that it will automatically set the end time to currrent time and will use default AWS profile in your configuration. that's it!

Another example:

  ```sh
  ttrail --start-time '12 hours ago' --end-time -- '11 hours ago' --profile dev-role
  ```

TTrail has an useful option of `--skip-service-events` to filter any events in the tree that is related to AWS service accounts. if your environment consist of many roles assigned to different AWS services that cause high volume of events, you can simply apply a display filter for those kinds of events via this option:


  ```sh
  ttrail --start-time '12 hours ago' --skip-service-events
  ```

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] First Alpha Release with Treeview and AWS Cloudtrail event history API client.
- [x] Ability to select Different AWS Profiles and Apply Display filter for Service Accounts.
- [ ] Filter Security Events.
- [ ] Read CloudTrail events from S3
- [ ] Advance Event Filtering and Alerting capabiltity 


See the [open issues](https://github.com/im4kv/TTrail/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


[![Stargazers repo roster for @im4kv/TTrail](https://reporoster.com/stars/im4kv/TTrail)](https://github.com/im4kv/TTrail/stargazers)



<!-- LICENSE -->
## License

Distributed under the Apache License 2.0. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>




<!-- CONTACT -->
## Contact

LinkedIn - [My LinkedIn Profile](https://www.linkedin.com/in/iman-khosravi-46912720/)

Project Link: [im4kv/TTrail](https://github.com/im4kv/TTrail)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/im4kv/TTrail.svg?style=for-the-badge
[contributors-url]: https://github.com/im4kv/TTrail/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/im4kv/TTrail.svg?style=for-the-badge
[forks-url]: https://github.com/im4kv/TTrail/network/members
[stars-shield]: https://img.shields.io/github/stars/im4kv/TTrail.svg?style=for-the-badge
[stars-url]: https://github.com/im4kv/TTrail/stargazers
[issues-shield]: https://img.shields.io/github/issues/im4kv/TTrail.svg?style=for-the-badge
[issues-url]: https://github.com/im4kv/TTrail/issues
[license-shield]: https://img.shields.io/github/license/im4kv/TTrail.svg?style=for-the-badge
[license-url]: https://github.com/im4kv/TTrail/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/iman-khosravi-46912720/
[ttrail-screenshot]: https://raw.githubusercontent.com/im4kv/TTrail/main/images/demo.gif