class Console {
	constructor(element) {
		this.element = element;
		this.buffer = '';
		this.history = [];
		this.historyIndex = -1;
    
    // create a full width inputline
    // <input id="console-input" type="text" placeholder="Type here..." onkeyup="handleKeyUp(event)"
    // style="background-color: #070404; color: white; border: none; font-family: monospace; outline: none; margin-left: 8px;">
    this.inputline = document.createElement('input')
    this.inputline.id = 'console-input';
    this.inputline.type = 'text';
    this.inputline.placeholder = 'Type here...';
    this.inputline.style.color = 'white';
    this.inputline.style.border = 'none';
    this.inputline.style.outline = 'none';
    this.inputline.style.width = '100%';
    this.inputline.style.backgroundColor = 'transparent';
    this.inputline.style.paddingLeft = '8px';

    // create a div that places $ to the left of the inputline
    // <div style="display: flex; flex-direction: row; align-items: center;">
    this.inputdiv = document.createElement('div');
    this.inputdiv.style.display = 'flex';
    this.inputdiv.style.flexDirection = 'row';
    this.inputdiv.style.alignItems = 'center';
    this.inputdiv.style.width = "100%";
    this.inputdiv.style.fontFamily = '"Ubuntu Mono", monospace;';
    this.inputdiv.style.fontSize = "1em"
    this.inputdiv.appendChild(document.createTextNode('$ '));
    this.inputdiv.appendChild(this.inputline);
    
    this.element.appendChild(this.inputdiv);
    this.init()
	}

	init() {
		this.inputline.addEventListener('keydown', (event) => this.handleKeyDown(event));
		this.inputline.addEventListener('input', () => this.handleInput());
		this.inputline.addEventListener('click', () => this.setFocus());
    this.setFocus()
	}

	handleKeyDown(event) {
		if (event.keyCode === 13) { // Enter
			event.preventDefault();
			const command = this.inputline.value;
			this.history.push(command);
			this.historyIndex = -1;
			this.buffer = '';
			this.runCommand(command);
		} 
		else if (event.keyCode === 38) { // Up
			event.preventDefault();
			if (this.historyIndex === -1) {
				this.historyIndex = this.history.length - 1;
			} else if (this.historyIndex > 0) {
				this.historyIndex--;
			}
			this.buffer = this.history[this.historyIndex] || '';
			this.updateBuffer();
		} 
		else if (event.keyCode === 40) { // Down
			event.preventDefault();
			if (this.historyIndex === -1) {
				this.buffer = '';
			} else if (this.historyIndex < this.history.length - 1) {
				this.historyIndex++;
				this.buffer = this.history[this.historyIndex];
			} else {
				this.historyIndex = -1;
				this.buffer = '';
			}
			this.updateBuffer();
		} 
		else if (event.keyCode === 76 && event.ctrlKey) {
			event.preventDefault();
			this.clear();
		}
	}

	handleInput() {
		// set the buffer to the current value of the inputline
    this.buffer = this.inputline.value;
	}

	async runCommand(command) {
		this.inputline.value = ''; // clear inputline
		this.addLine(`$ ${command}`, 'console-command');
		const output = this.execute(command)
		
		// change color of `console-input` and set text to 'sent request, waiting...'
		const oldcolor = this.inputline.style.color;
		const oldvalue = this.inputline.value;
		this.inputline.style.color = 'yellow';
		this.inputline.value = 'sent request, waiting...';
		// stop allowing input
		this.inputline.disabled = true;

    output.then((data) => {
      this.addLine(data);
		  this.scrollToBottom();
			this.inputline.style.color = oldcolor
			this.inputline.value = oldvalue
			this.inputline.disabled = false;
    })
	}

	execute(command) {
		// send request to /console?command=`${command}`
    // return the response as a promise
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', '/console?command=' + encodeURIComponent(command));
      xhr.onload = () => {
        if (xhr.status === 200) {
          resolve(xhr.response);
        } else {
          reject(new Error(`Request failed with status ${xhr.status}`));
        }
      };
      xhr.onerror = () => {
        reject(new Error('Request failed'));
      };
      xhr.send();
    })
	}

	add(element){
		this.element.insertBefore(element, this.inputdiv);
		// if paddingbottom is greater than offsetheight, reduce it by offsetheight
		// padding is maintained to allow user to clear screen with ctrl+l		
    const curpadding = parseInt(this.element.style.paddingBottom);
    if(curpadding > element.offsetHeight) {
      const newpadding = curpadding - element.offsetHeight;
      this.element.style.paddingBottom = `${newpadding}px`;
    }
	}

	addLine(line, clazz = null) {
		const pre = document.createElement('pre');
		pre.textContent = line;
		pre.style.color = 'white';
		pre.style.margin = '0';
		pre.style.padding = '0';
		pre.style.fontFamily = '"Ubuntu Mono", monospace;';
		pre.style.fontSize = "1em"
		if(clazz != null)
			pre.classList.add(clazz);
		this.add(pre);
	}

	updateBuffer() {
		this.inputline.value = this.buffer;
		this.setFocus();
	}

	setFocus() {
		// const range = document.createRange();
		// const selection = window.getSelection();
		// range.selectNodeContents(this.inputline);
		// range.collapse(false);
		// selection.removeAllRanges();
		// selection.addRange(range);
		this.inputline.focus();
	}

	scrollToBottom(addoffset = false) {
		// scroll to the bottom of the console
    consoleContainer.scrollTop = consoleContainer.scrollHeight;
	}

	clear() {
    const consoleContainer = document.querySelector('#console-container');
    // find the number of lines that will fit in the consolecontainer
    const lineheight = this.inputdiv.offsetHeight;
    const offset = consoleContainer.offsetHeight - lineheight*2
    // increase bottom padding of the console to push inputline to top
    this.element.style.paddingBottom = `${offset}px`;

		this.scrollToBottom();
		this.setFocus();
	}
}

const consoleElement = document.querySelector('#console');
const consoleInstance = new Console(consoleElement);

// if the consoleContainer gets a click event, set the focus to the inputline
const consoleContainer = document.querySelector('#console-container');
consoleContainer.addEventListener('click', () => consoleInstance.setFocus());