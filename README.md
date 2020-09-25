# hydracodegenerator
### Generate Hydra code randomly. Livecode from your phone.
![Hydra Code Generator](https://github.com/alecominotti/hydracodegenerator/blob/master/hcg.png?raw=true)  

<br>

###### English
- HCG is an app that randomly generates code in Hydra sintax. The sources, functions, the amount of them and the values of their arguments are all generated randomly (within customizable lower and upper bounds). You can also specify the probability of generating certain arguments and which elements you want in your generated code and which you don't. The Live Session Mode allows you tu execute in Hydra the generated code, and also to livecode from this app.
HCG aims to allow you to explore the infinite creation posibilities that Hydra provides, combining them with the art of randomness and the user customization, allowing you to find inspiration, new ideas or just pass the time.

###### Español
HCG es una app que genera código en sintaxis de Hydra de manera aleatoria. Las sources, functions, la cantidad de ellas y los valores de sus argumentos son todos generados aleatoriamente (dentro de rangos personalizables). También puedes especificar la probabilidad de que se generen determinados argumentos y establecer cuáles elementos quieres en tu código generado y cúales no. El Live Session Mode te permite ejecutar en Hydra el código generado, así como también hacer livecoding desde esta app. HCG tiene como objetivo ayudarte a explorar las infinitas posibilidades de creación que provee Hydra, combinándolas con el arte de lo aleatorio y la personalización del usuario, para encontrar inspiración, nuevas ideas o simplemente pasar el rato.\
En la pestaña de ayuda dentro de la app está la documentación completa en español.

<br>



### Installation instructions
You must have [Python 3](https://www.python.org/downloads/ "Python 3 Download") and [Google Chrome](https://www.google.com/chrome/ "Google Chrome Download") installed.

#### Linux and Mac:

- Open up a terminal and clone the directory, typing:
	<pre>git clone https://github.com/alecominotti/hydracodegenerator.git</pre>
- Enter the directory:	
	<pre>cd hydracodegenerator</pre>
- Install dependencies:	
	<pre>python3 -m pip install -r requirements.txt</pre>
- Run the app:	
	<pre>python3 manage.py runserver</pre>

<br>

#### Windows:

- Open up a terminal (program called "cmd") and clone the directory, typing:
	<pre>git clone https://github.com/alecominotti/hydracodegenerator.git</pre>
- Enter the directory:	
	<pre>cd hydracodegenerator</pre>
- Install dependencies:	
	<pre>py -m pip install -r requirements.txt</pre>
- Run the app:	
	<pre>py manage.py runserver</pre>


<br>

#### Then go to [http://127.0.0.1:8000/](http://127.0.0.1:8000) in the browser.

<br>

### Live Session Mode
If you turn this on, Hydra will be opened in a web browser, and you will be able control it from this app. Live Session mode allows you to write and run random generated code automatically, and also to livecode in Hydra without touching the window where Hydra is open. Since this is a web app, you can control and livecode in Hydra remotely, from a phone, tablet or other computer in your local network.

If you wish to livecode remotely from a phone, table or other computer, you need to run the app with the following command:


<code>python3 manage.py runserver LOCAL_IP:PORT</code>


- You can choose any port number you want between 1024 and 65535.
- Get your local IP in Linux terminal: <code>hostname -I</code>
- Get your local IP in Mac terminal: <code>ipconfig getifaddr en0</code> 
- Get your local IP in Windows terminal: <code>ipconfig | findstr IPv4</code>

Example: if your local IP is "192.168.0.15" you could start the app with <code>python3 manage.py runserver 192:168.0.15:6969</code> (On Windows replace 'python3' with 'py'). Then in your phone browser go to 192.168.0.15:6969


### Hide Keys
This toggle lets your hide or show the code in the Hydra window if a Live Session is active.


### Auto Send
If you turn this on, the new generated code will automatically be written and executed in Hydra when you click the Generate Code button, if a Live Session is active. Leave this turned off if you want to livecode from this app.


### Generate Code
Click this button to generate new code with the parameters you set. If a Live Session is active and Auto Send is on, the new generated code will be written and executed in Hydra automatically. Don't worry about loosing them. All generated codes are saved in a text file called "generatedCodeHistory.txt", located on the root folder of the app.


### Send Code to Hydra
Click this button to execute the code of the editor in Hydra. This button is useful for remote livecoding and it's only available if a Live Session is active.You can also execute your code by clicking Ctrl+Shift+Enter.

<br>

## Customize randomness:


### Min Function Amount
Here you specify the minimum amount of functions that the generated code can have

### Max Function Amount
Here you specify the maximum amount of functions that the generated code can have

HCG will generate a random number between these two values and that number will be the amount of functions of the generated code. If you set the same number for both values, the amount of functions will always be the same.

    Example: Min function amount: 3. | Max Function amount: 3. Possible output:

    osc(2, 1, 1)  // This is a source
      .colorama(0.5)  // This is a function
      .luma(0.2)  // This is a function
      .pixelate(2.5)  // This is a function
    .out(o0)


### Min Argument Value
Here you specify the minimum value that the arguments of the generated code can have

### Max Argument Value
Here you specify the maximum value that the arguments of the generated code can have

HCG will generate a random number between these two values for every argument of the sources and functions of the generated code. If you set the same number for both values, the arguments will always be the same.

_Note: solid, brightness, luma, color, invert, posterize, thresh, add, blend, mult and modulate amounts generate they own random value between 0 and 1, to avoid possible "useless functions". Anyways, you can manually change the values and run the code again if you want._

    Example: Min argument value: 10. | Max Argument value: 15. Possible output:

    osc(11, 10.5, 13.2)
      .colorama(14.9)  // This is a function
      .saturate(12.7)  // This is a function
      .pixelate(10.3)  // This is a function
      .brightness(0.4)  // This is a function that will generate its own argument value between 0 and 1
      .modulate(o0, 0.2)  // This is a function that will generate its own modulation amount value between 0 and 1
    .out(o0)


### Arrow Function Probability
Here you specify the probability of generating an arrow function as an argument value, that uses Math functions like sin, cos and tan

If you set this value to 100, every argument will have a 100% chance of being an arrow function, so they will all be arrow functions. This does not apply to functions that generate their own value between 0 and 1.

    Example: Arrow Function probability: 100. Possible output:

    osc(() => Math.sin(time), () => Math.cos(time * 0.3), () => Math.tan(time))
      .colorama(() => Math.sin(time * 0.5))
      .pixelate(() => Math.cos(time * 0.7))
    .out(o0)


### Mouse Function Probability
Here you specify the probability of generating a mouse arrow function as an argument value

If you set this value to 100, every argument will have a 100% chance of being a mouse arrow function, so they will all be mouse arrow functions. This does not apply to functions that generate their own value between 0 and 1.

    Example: Mouse Function probability: 100. Possible output:

    osc(() => mouse.x, () => mouse.x), () => mouse.y)
      .colorama(() => mouse.x)
      .pixelate(() => mouse.y)
    .out(o0)


### Modulate itself Probability:
Here you specify the probability of setting "o0" as the first argument of any modulate function.

If you set this value to 100, every generated modulate function will have a 100% chance of having "o0" as its first argument, so they will all modulate the output with itself.

    Example: Modulate itself probability: 100. Possible output:

    osc(10, 0.5, 1)
      .colorama(1)
      .modulateScale(o0, 0.3)
      .modulate(o0, 0.8)
    .out(o0)


### Exclusive sources
Here you specify the only sources you want in the generated code.

For instance, if you only select "osc", every generated source will be an oscillator.

    Example: only "osc" selected. Possible output:

    osc(10, 0.5, 1)
      .colorama(1)
      .modulateScale(osc(12, 2, 3), 0.3)
      .modulate(osc(1, 0.2, 1.5), 0.8)
    .out(o0)


### Exclusive Functions
Here you specify the only functions you want in the generated code.

For instance, if you only select "colorama", every generated function will be a colorama.

    Example: only "colorama" selected. Possible output:

    voronoi(10, 0.5, 1)
      .colorama(1)
      .colorama(0.3)
      .colorama(3)
    .out(o0)


### Ignore List
Here you specify the elements (sources and functions) that you don't want in the generated code.

For instance, if you select "luma", the generated code will never contain a luma function.

    Example: only "luma" selected. Possible output:

    voronoi(10, 0.5, 1)
      .colorama(1)
      .brigthness(0.1)
      .modulate(o0, 0.4)
    .out(o0)
    
</br>

#### Links:
	
- Hydra, by Olivia Jack:
	  [https://github.com/ojack/hydra](https://github.com/ojack/hydra "Hydra, By Olivia Jack")
  
</br>

------------------------------------------------------------------------------------------------------------------------------------------
##### Ale Cominotti - 2020
