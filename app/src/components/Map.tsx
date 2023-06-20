import { useEffect, useState, useRef, useMemo } from 'react';
import { Alert, View, StyleSheet, Text, TextInput, FlatList, TouchableOpacity, Keyboard } from 'react-native';
import MapView , { Marker } from 'react-native-maps';
import { FontAwesome } from '@expo/vector-icons'
import * as Location from 'expo-location'
import { BottomSheetModal, BottomSheetModalProvider } from '@gorhom/bottom-sheet';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { Dimensions } from 'react-native';

export function Map(props) {
  type CoordProps = {
    latitude: number;
    longitude: number;
  }

  type LocationCoordProps =  CoordProps & {
    id: string
  } 

  const parkings: LocationCoordProps[] = [{
    id: 'a',
    latitude: 41.17796324211171, 
    longitude: -8.60891994096156
  },
   {
    id: 'b',
    latitude: 41.17786497596217, 
    longitude: -8.608226428692205
   }, {
    id: 'c',
    latitude: 41.17832324568314, 
    longitude: -8.608156691263558
   }, {
    id: 'd',
    latitude: 41.1788158315874, 
    longitude: -8.608623395593737
   }]

   const ItemSeparatorView = () => {
    return (
      // Flat List Item Separator
      <View
        style={{
          height: 0.5,
          width: '100%',
          backgroundColor: '#C8C8C8',
        }}
      />
    );
  };
  const ItemView = ({item}: any ) => {
    return (
      // Flat List Item
      <TouchableOpacity  style={styles.itemStyle} onPress={() => handleSeletItem(item)}>
        <Text>{item.id.toUpperCase()} - ISEP Parking {item.id.toUpperCase()}</Text>
      </TouchableOpacity >
    );
  };

  const handleSeletItem = (item : LocationCoordProps) => {
    props.navigation.navigate('selectspot',{item})
  };

  const searchFilterFunction = (text: string) => {
    // Check if searched text is not blank
    if (text) {
      // Inserted text is not blank
      // Filter the masterDataSource and update FilteredDataSource
      const newData = parkings.filter(function (item) {
        // Applying filter for the inserted text in search bar
        const itemData = item.id
          ? item.id.toUpperCase()
          : ''.toUpperCase();
        const textData = text.toUpperCase();
        return itemData.indexOf(textData) > -1;
      });
      setFilteredDataSource(newData);
      setSearch(text);
    } else {
      // Inserted text is blank
      // Update FilteredDataSource with masterDataSource
      setFilteredDataSource(parkings);
      setSearch(text);
    }
  };

  const bottomSheetModalRef = useRef(null);
  const snapPoints = useMemo(() => ["40%"], []);
 
  const openModal = () => {
      bottomSheetModalRef.current.present();
    };


  const [currentLocation, setCurrentLocation] = useState<CoordProps | null>(null)
  const [search, setSearch] = useState('');
  const [filteredDataSource, setFilteredDataSource] = useState<LocationCoordProps[]>(parkings);
  
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
    <GestureHandlerRootView style={{flex: 1}}> 
      <BottomSheetModalProvider>
        <View style={styles.container}>
          {

            currentLocation && <MapView style={styles.map}
            initialRegion={{
              //posição no mapa - to be replaced with current location
              latitude: 41.17880410608253, 
              longitude: -8.609241948747831,
              //latitude: currentLocation.latitude, 
              //longitude: currentLocation.longitude,
              // aproximação mostrada no mapa
              latitudeDelta: 0.005,
              longitudeDelta: 0.005
            }}
            >
            {
              <Marker identifier='origin' coordinate={{          
                latitude: 41.17880410608253, 
              longitude:  -8.609241948747831}
              }>
                <FontAwesome name="car" size={28} color="green" />
              </Marker> }
              { parkings.map((item)=> (
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
          <View style={styles.searchContainer}>
            <TextInput
                  style={styles.textInputStyle}
                  onChangeText={(text) => searchFilterFunction(text)}
                  value={search}
                  onTouchStart={openModal}
                  underlineColorAndroid="transparent"
                  placeholder="Search Destinations"
                />
              <BottomSheetModal
                ref={bottomSheetModalRef}
                index={0}
                snapPoints={snapPoints}
                enablePanDownToClose={true}
              >
                <TextInput
                  style={styles.textInputStyle}
                  onChangeText={(text) => searchFilterFunction(text)}
                  value={search}
                  underlineColorAndroid="transparent"
                  placeholder="Search Destinations"
                />
                <FlatList
                  data={filteredDataSource}
                  keyExtractor={(item, index) => index.toString()}
                  ItemSeparatorComponent={ItemSeparatorView}
                  renderItem={ItemView}
                  keyboardShouldPersistTaps="always" // Manter o teclado aberto ao tocar na lista
                  onTouchStart={() => Keyboard.dismiss()} // Fechar o teclado quando tocar na lista
                />
              </BottomSheetModal>
          </View>
        </View>
      </BottomSheetModalProvider>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  map: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
  },
  marker: {
    width: 32,
    height: 32,
    backgroundColor: "transparent",
    borderColor: "blue",
    borderWidth: 2,
    borderStyle: 'solid',
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center'
  },
  text: {
    position: 'absolute',
    fontSize: 24,
    color: 'red',
    fontWeight: 'bold',
  },
  searchContainer: {
    position: 'absolute',
    zIndex: 1,
    width: '100%',
    bottom: 0,
    backgroundColor: 'white'
  },
  itemStyle: {
    padding: 10,
  },
  textInputStyle: {
    height: 40,
    borderWidth: 1,
    paddingLeft: 20,
    margin: 5,
    borderColor: '#009688',
    backgroundColor: '#FFFFFF',
  },
});