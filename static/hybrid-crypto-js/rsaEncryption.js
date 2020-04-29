function encryptMe(){
			var message="Hello world";
			var encrypted=crypt.encrypt(publicKey, message);
			document.getElementByID("encryptedMessage").value=encrypted;
		}

function generateKeys(){
			//initializing RSA-class
			var entropy=Math.random() * 1000000;
			var rsa=new RSA({entropy: entropy});

			//Generating RSA key pair 4096 bit key
			rsa.generateKeypair(function(keypair){
				var publicKey=keypair.publicKey;
				var privateKey=keypair.privateKey;

				localStorage.generatedPublicKey=publicKey;
				localStorage.generatedPrivateKey=privateKey;
				
				document.getElementById("publicKey").innerHTML=localStorage.generatedPublicKey;
				document.getElementById("hiddenPublicKey").value=publicKey;
				//document.getElementById("privateKey").innerHTML=privateKey;

				alert("done")
			});
			/*Generate 1024 bit RSA bit key pair
			rsa.generateKeypair(function(keypair){
				var publicKey=keypair.publicKey;
				var privateKey=keypair.privateKey;
			}, 1024);

			*/
		}

