import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, AlertController } from 'ionic-angular';

import { HttpEcuacionesUnaVariableProvider } from '../../../providers/http-ecuaciones-una-variable/http-ecuaciones-una-variable';


/**
 * Generated class for the BusquedasIncrementalesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-busquedas-incrementales',
  templateUrl: 'busquedas-incrementales.html',
})
export class BusquedasIncrementalesPage {

  private apiUrl = 'http://165.227.197.6:8080/api/busquedas/';

  private dataSubmit = {}

  private dataReceivedGet = {};
  private dataReceivedPost = {};

  private root = [];
  private roots = [];
  private visibleRoot;
  private visibleRoots;

  private tableTitles  = ['i','x','f(x)']
  private tableContent = []
  private visibleTable;
  
  constructor(public navCtrl: NavController, public navParams: NavParams, public alertCtrl: AlertController, public httpEcuacionesUnaVariableProvider : HttpEcuacionesUnaVariableProvider) {
    this.dataSubmit['fx'] = '';
    this.dataSubmit['x0'] = '';
    this.dataSubmit['delta'] = '';
    this.dataSubmit['nIters'] = '';

    this.visibleTable = false;
    this.visibleRoot  = false;
    this.visibleRoots = false;

    this.getServer();
  
  } 

  private presentAlert() {
    let alert = this.alertCtrl.create({
      title: '¿Qué debo hacer?',
      subTitle: ` <p>Ingresa los siguientes Datos:</p>
                  <ul>
                    <li> <b>Función:</b> La función que desea evaluar</li>
                    <li> <b>X0:</b> Valor Inicial de X </li>
                    <li><b>Delta:</b> Tamaño de intervalo para efectuar las búsquedas</li>
                    <li><b># Iteraciones:</b> Número máximo de iteraciones que se ejecuta el método</b> </li>
                  </ul>`,
      buttons: ['Entendido']
    });
    alert.present();
  }

  submitForm() {
    console.log(this.dataSubmit)
    this.verification();
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad BusquedasIncrementalesPage');
  }

  verification(){
   if (this.dataSubmit['fx'] == ''){
    this.showAlert('f(x)');
   }else if (this.dataSubmit['x0'] == ''){
     this.showAlert('x Inicial');
   }else if (this.dataSubmit['delta'] == ''){
     this.showAlert('delta');
   }else if(this.dataSubmit['nIters'] == ''){
    this.showAlert('Num. Iters');
   }else{
    console.log("Campos verificados y completos.");
    this.postServer();
   }   
  }


  showAlert(value:string) {
    let alert = this.alertCtrl.create({
      title: 'Error!',
      subTitle: 'El campo ' + value + ' no puede estar vacío!',
      buttons: ['OK']
    });
    alert.present();
  }


  //Zona de get y post

  private completeTable(){
    this.tableContent = this.dataReceivedPost['iteraciones'];
    console.log(this.tableContent.length);
    if (this.tableContent.length != 0){
      this.root = this.dataReceivedPost['raices'];
      this.roots = this.dataReceivedPost['intervalos']
      console.log("Raices " + this.root);
      console.log("Intervalos " + this.roots);
      console.log("Numero de raices: " + this.root.length);
      console.log("Numero de intervalos: " + this.roots.length);
      console.log("Numero de raices dif 0: " + (this.root.length != 0 ));
      console.log("Numero de intervalos dif 0: " + (this.roots.length != 0));

      this.visibleTable = true;

      if (this.root.length != 0) {
        this.visibleRoot  = true;
      }

      if (this.roots.length != 0) {
        this.visibleRoots  = true;
      }
      
      console.log("Visibilidad de raiz: " + this.visibleRoot);
      console.log("Visibilidad de intervalos: " + this.visibleRoots);
    } else {
      this.visibleTable = false;
      this.visibleRoot  = false;
    }    
  }

  //Zona de get y post

  public getServer() {
    this.httpEcuacionesUnaVariableProvider.get(this.apiUrl)
    .then(data => {
      this.dataReceivedGet = data;
      console.log("Realice el GET-BUSQ-INCREM ->");
      console.log(JSON.stringify(data));
      console.log(this.dataReceivedGet);
      console.log(typeof(this.dataReceivedGet));
    }, (err) => {
      console.log("Problema al hacer GET-BUSQ-INCREM");
      console.log(err);
    });
  }


  public postServer() {
    this.httpEcuacionesUnaVariableProvider.post(this.dataSubmit, this.apiUrl)
    .then(result => {
      this.dataReceivedPost = result; 
      console.log(this.dataReceivedPost);
      this.completeTable();
      console.log("Realice el POST-BUSQ-INCREM");
    }, (err) => {
      console.log("Problema al hacer POST-BUSQ-INCREM");
      console.log(err);
    });
  }
}
