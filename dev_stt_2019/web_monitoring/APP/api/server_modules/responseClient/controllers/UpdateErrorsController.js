'use strict';
var ErrorModel = require('../models/Errors.js');

var UpdateErrorsController = function init(modules) {
  var loadErrorDefault = function(){
    /****************/
    console.log('Installer Errors');

    var error;
    error = new ErrorModel({
          code : '000',
          message : 'Errore non riconosciuto'
        });
    error.save();
    error = new ErrorModel({
          code : '001',
          message : 'Generale'
        });
    error.save();

    error = new ErrorModel({
          code : '002',
          message : 'Non trovato'
        });
    error.save();

    error = new ErrorModel({
          code : '004',
          message : 'Non Autorizzato'
        });
    error.save();
    error = new ErrorModel({
          code : '005',
          message : 'Tempo Scaduto'
        });
    error.save();
    error = new ErrorModel({
          code : '006',
          message : 'Password errata'
        });
    error.save();
    error = new ErrorModel({
          code : '007',
          message : 'Dati inseriti errati'
        });
    error.save();
    error = new ErrorModel({
          code : '008',
          message : 'Dati Mancanti'
        });
    error.save();
    error = new ErrorModel({
          code : '009',
          message : 'File Non Trovato'
        });
    error.save();
    error = new ErrorModel({
          code : '010',
          message : 'Problema durante il salvataggio delle informazioni'
        });
    error.save();
    error = new ErrorModel({
          code : '011',
          message : 'Negozio già esistente'
        });
    error.save();
    error = new ErrorModel({
          code : '012',
          message : 'Utente già esistente'
        });
    error.save();
    error = new ErrorModel({
          code : '013',
          message : ''
        });
    error.save();
    /****************/
  };
  loadErrorDefault();
};

module.exports = UpdateErrorsController;
