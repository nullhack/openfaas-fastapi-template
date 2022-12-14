<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">openfaas-fastapi-template</h3>

  <p align="center">
    Python template for OpenFAAS functions using FastAPI
    <br />
    <a href="https://nullhack.github.io/openfaas-fastapi-template/readme.html"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nullhack/openfaas-fastapi-template/issues">Report Bug</a>
    ·
    <a href="https://github.com/nullhack/openfaas-fastapi-template/issues">Request Feature</a>
  </p>
</div>



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
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Python template for OpenFAAS functions using FastAPI. This template has two flavours, a simple project using fastapi and a more complex with authentication using JWE (encrypted JWT) for improved security.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To run this project locally, you will need to install the prerequisites and follow the installation section.

### Prerequisites

* This Project depends on [OpenFAAS](https://www.openfaas.com/)
  ```sh
  curl -sSL https://cli.openfaas.com | sudo -E sh
  ```

### Installation

1. Pull the template
   ```sh
   faas template pull https://github.com/nullhack/openfaas-fastapi-template/
   ```
2. Create a new function
   ```sh
   faas new --lang openfaas-fastapi-template myf
   ```
   
   or
   
   ```sh
   faas new --lang openfaas-fastapi-jwe-template myf
   ```
   
3. Include the function name as environment variable into the `myf.yml` file
   ```sh
   ...
       environment:
         FUNCNAME: myf
   ...
   ```
4. build and publish the function to the server
   ```sh
   faas up -f myf.yml
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Alternative Usage

It's possible to directly use the template without *OpenFAAS* or to test it before pushing to the server.

*  Install requirements
   ```sh
   pip install poethepoet poetry
   # go to the function folder
   poe install-dev
   ```

*  Run tests
   ```sh
   poe test
   ```

*  Generate API documentation
   ```sh
   poe doc
   ```

*  Build a docker image for tests
   ```sh
   poe docker-build --target test --build-tag 3.10-alpine
   docker run -ti --rm handler:test-3.10-alpine
   ```

*  Build a docker image to run the root files only without running any test
   ```sh
   poe docker-build --target prod --build-tag 3.10-alpine --no-test
   docker run -ti --rm handler:prod-3.10-alpine
   ```
   

_For more examples, please refer to the [Documentation](https://nullhack.github.io/openfaas-fastapi-template/readme.html)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Improve JWE template coverage

See the [open issues](https://github.com/nullhack/openfaas-fastapi-template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Eric Lopes - [@nullhack](https://github.com/nullhack)

Project Link: [https://github.com/nullhack/openfaas-fastapi-template/](https://github.com/nullhack/openfaas-fastapi-template/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This project was created using cookiecutter and nullhack's python-project-template:

* [nullhack's python-project-template](https://github.com/nullhack/python-project-template/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/nullhack/openfaas-fastapi-template/blob/main/LICENSE) for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/nullhack/openfaas-fastapi-template.svg?style=for-the-badge
[contributors-url]: https://github.com/nullhack/openfaas-fastapi-template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/nullhack/openfaas-fastapi-template.svg?style=for-the-badge
[forks-url]: https://github.com/nullhack/openfaas-fastapi-template/network/members
[stars-shield]: https://img.shields.io/github/stars/nullhack/openfaas-fastapi-template.svg?style=for-the-badge
[stars-url]: https://github.com/nullhack/openfaas-fastapi-template/stargazers
[issues-shield]: https://img.shields.io/github/issues/nullhack/openfaas-fastapi-template.svg?style=for-the-badge
[issues-url]: https://github.com/nullhack/openfaas-fastapi-template/issues
[license-shield]: https://img.shields.io/badge/license-MIT-green?style=for-the-badge
[license-url]: https://github.com/nullhack/openfaas-fastapi-template/blob/main/LICENSE

