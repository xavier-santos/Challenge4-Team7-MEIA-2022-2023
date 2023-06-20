import { useEffect, useState } from 'react';
import { Alert, View, Text } from 'react-native';
import MapView , { Marker } from 'react-native-maps';
import { FontAwesome } from '@expo/vector-icons'
import * as Location from 'expo-location'
import { CoordProps, LocationCoordProps, MapProps } from 'src/types/types';
import { styles } from '../styles/styles';

export function Map({ markers }: MapProps) {
  const [currentLocation, setCurrentLocation] = useState<CoordProps | null>(null)
  
  useEffect(()=> {
    let subscription: Location.LocationSubscription
    Location.requestForegroundPermissionsAsync()
    .then(({status}) => {
      if(status !== 'granted'){
        Alert.alert("Habilite a permissão para obter a localização");
        return
      }

      Location.watchPositionAsync({
        accuracy: Location.LocationAccuracy.High,
        timeInterval: 1000,
        distanceInterval: 1,
      }, (location) => {
        setCurrentLocation(location.coords)
      }).then((reponse => subscription = reponse));
    })

    return () => {
      if(subscription){
        subscription.remove()
      }
    }

  }, [])

  return (
        <View style={styles.container}>
          {

            currentLocation && <MapView style={styles.map}
            initialRegion={{
              //posição no mapa - to be replaced with current location
              latitude: markers[0].latitude, 
              longitude: markers[0].longitude,
              //latitude: currentLocation.latitude, 
              //longitude: currentLocation.longitude,
              // aproximação mostrada no mapa
              latitudeDelta: 0.002,
              longitudeDelta: 0.002
            }}
            >
            {
              <Marker identifier='origin' coordinate={{          
                latitude: 41.17880410608253, 
              longitude:  -8.609241948747831}
              }>
                <FontAwesome name="car" size={28} color="green" />
              </Marker> }
              { markers.map((item: LocationCoordProps)=> (
                <Marker key={item.id} identifier={item.id} 
                  coordinate={{          
                  latitude: item.latitude, 
                  longitude: item.longitude
                }}>
                  <View style={styles.marker}>
                    <Text  style={styles.text} >
                    {item.id.toUpperCase()}
                    </Text>
                  </View>
                </Marker>
              ))
              }
            </MapView>
          }
        </View>
  );
}
