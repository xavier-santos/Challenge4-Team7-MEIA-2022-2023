import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Text, View } from 'react-native';
import { Map } from '../components/Map';
import FontAwesome from 'react-native-vector-icons/FontAwesome';
import useBLE from '../composables/useBLE';
import { styles } from '../styles/styles';
import { useRoute } from '@react-navigation/native';
import { LocationCoordProps } from '../types/types';
import { BottomSheetModal, BottomSheetModalProvider } from '@gorhom/bottom-sheet';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export function Directions()  {
  const route = useRoute()
  const { markers } = route.params
  const [hasArrived, setHasArrived] = useState(false);

  const destination: LocationCoordProps = {
    id: 'P',
    latitude: markers[0].latitude,
    longitude: markers[0].longitude
  }
  const {requestPermissions, scanForPeripherals, distance} = useBLE();
  const [distanceFromSpot, setDistanceFromSpot] = useState(distance); // or however you get your distance

  const scanForDevices = () => {
    requestPermissions(isGranted => {
      if (isGranted) {
        scanForPeripherals();
      }
    });
  };

  const bottomSheetModalRef = useRef(null);
  const snapPoints = useMemo(() => ["10%"], []);

  useEffect(() => {
    if (distance != -1 && distance < 0.09) {
      setHasArrived(true);
    }
  }, [distance]);

  useEffect(()=> {
    scanForDevices();
    bottomSheetModalRef.current.present();
  }, [])

  return (
        <GestureHandlerRootView style={{flex: 1}}> 
        <BottomSheetModalProvider>
          <View style={styles.container}>
          <Map markers={markers} polylineCoords={destination}  />
            <View style={styles.searchContainer}>
                <BottomSheetModal
                  ref={bottomSheetModalRef}
                  index={0}
                  snapPoints={snapPoints}
                  enablePanDownToClose={false}
                >
                  <View style={styles.selectSpotWrapper}>
                  {!hasArrived && 
                    <Text style={{fontSize: 18, color: 'black'}}>Distance to spot: {distance}</Text>
                  } 
                  {hasArrived && 
                    <View>
                      <FontAwesome name="check" size={32} color="green" />
                      <Text>You've arrived!</Text>
                    </View>
                  }   
                  </View>
                </BottomSheetModal>
            </View>
          </View>
        </BottomSheetModalProvider>
      </GestureHandlerRootView>
  );
};

