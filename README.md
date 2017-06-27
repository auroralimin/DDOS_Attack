# DDOS_Attack
Esse projeto foi desenvolvido como requisito da disciplina Teleinformática e Redes 2, da Universidade de Brasília (UnB).

## Ataques
Esse projeto visa implementar dois tipos de ataque de negação de serviço e então distribuí-los: O *[SYN Flood][SYNFLOOD]* e o *[HTTP Post][HTTPOST]*.

### SYN Flood
Ataque que manda uma sucessão de requisições do tipo SYN de modo a tornar o servidor indisponível por fazê-lo tentar um "three-way handshake" que nunca será finalizado

### HTTP Post
Estabelece numerosas conexões via HTTP com o servidor, cada conexão contendo um "content length" de valor alto. Entretanto, em vez de mandar todos os dados de uma vez, manda-os de um em um caracter durante um longo período de tempo.

## Servidor para testes
Para testes constrolados, será usado um servidor HTTP Apache como vítima do ataque. Para instalá-lo, recomenda-se *[esse tutorial para o Ubuntu][UBUNTU]*, *[esse tutorial para demais sistemas Unix-like][UNIX]* e *[esse tutorial para Windows][WINDOWS]*.

## Metodologia de desenvolvimento

Esse projeto está sendo desenvolvido usando a metodologia Extreme Programming (*[XP][XP]*). As votações a respeito da complexidade dessas histórias estão sendo feitas através da plataforma do Plan IT Poker (e podem ser acessadas *[aqui][PLANITPOKER]*). Por fim, as tarefas criadas a partir dessas histórias possuem referência a qual história elas possuem nas *[Issues][ISSUES]* criadas para elas.

## Diretrizes do projeto

### Estilo do código
O código será escrito com o padrão "Camel Case". 
Como padrão, as variáveis, abstrações e nomes no código serão dadas em inglês e toda a documentaço será feita em português. 

A linguagem de programação utilizada é o Python e o projeto segue diretrizes (*[Guidelines][GUIDELINES]*) para programar nessa linguagem feitas pelos próprios desenvolvedores da linguagem.

### Documentação no Git
As tarefas a serem desenvolvidas serão geradas como *[Issues][ISSUES]* e as tarefas macros a serem feitas estão específicadas nos
*[Projetos][PROJECTS]* (ex: TODO e User Stories).

As mensagens de commit seguem um padrão especificado *[aqui][GITMSG]*.

[XP]: http://www.extremeprogramming.org/
[USERSTORY]: https://github.com/auroralimin/DDOS_Attack/projects/1
[ISSUES]: https://github.com/auroralimin/DDOS_Attack/issues
[GUIDELINES]: https://www.python.org/dev/peps/pep-0008/
[PROJECTS]: https://github.com/auroralimin/DDOS_Attack/projects
[GITMSG]: https://github.com/erlang/otp/wiki/Writing-good-commit-messages
[UBUNTU]: https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-16-04
[UNIX]: http://httpd.apache.org/docs/2.4/install.html
[WINDOWS]: http://httpd.apache.org/docs/2.4/platform/windows.html
[HTTPOST]: https://www.acunetix.com/blog/articles/http-post-denial-service/
[SYNFLOOD]: https://www.incapsula.com/ddos/attack-glossary/syn-flood.html
[PLANITPOKER]: http://www.planitpoker.com/board/#/room/e3294ada6176461e8bb31fcf4ef48f10

