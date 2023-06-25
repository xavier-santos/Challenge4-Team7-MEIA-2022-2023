import React, { useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';

import init from 'react_native_mqtt';
import AsyncStorage from '@react-native-async-storage/async-storage';
import config from '../../config.json'

export function Arrived() {

    const [parked, setParked] = useState(false);
    const [left, setLeft] = useState(false);

    init({
      size: 10000,
      storageBackend: AsyncStorage,
      defaultExpires: 1000 * 3600 * 24,
      enableCache: true,
      reconnect: true,
      sync: {},
    });

    function onConnect() {
      client.subscribe('display_value', { qos: 0 });
      console.log("onConnect");
    }

    function onConnectionLost(responseObject) {
      if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
      }
    }

    function onMessageArrived(message) {
      console.log("onMessageArrived:" + message.payloadString);
      if (message.payloadString === '0'){
            setParked(true)
      } else if(message.payloadString === '1'){
            setLeft(true)
      }
    }

    function onFailure(err) {
        console.log('Connect failed!', err);
    }

    const client = new Paho.MQTT.Client(config.ip_adress, 9001, 'display_value');
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived
    client.connect({ onSuccess: onConnect, useSSL: false, timeout: 300, onFailure: onFailure });


  return (
    <View style={styles.container}>
        {!parked && !left &&    
        <View>
            <FontAwesome style={styles.icon} name="check-circle" size={150} color="green" />
            <Text style={styles.message}>You've arrived!</Text>
        </View>
        }
        {parked && !left &&    
        <View>
            <FontAwesome name="car" size={150} color="green" />
            <Text style={styles.message}>Parked!</Text>
        </View>
        }
        {parked && left &&    
        <View>
            <FontAwesome style={styles.icon} name="check-circle" size={150} color="green" />
            <Text style={styles.message}>Finished!</Text>
            <Text style={styles.payed}>$10 Payment completed</Text>
        </View>
        }
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ffffff',
  },
  icon: {
    textAlign: 'center'
  },
  message: {
    fontSize: 32,
    fontWeight: 'bold',
    marginTop: 30,
    textAlign: 'center'
  },
  payed: {
    fontSize: 28,
    fontWeight: 'bold',
    marginTop: 30,
    textAlign: 'center'
  },
});