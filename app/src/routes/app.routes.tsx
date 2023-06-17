import { createNativeStackNavigator } from '@react-navigation/native-stack'

import { Map } from '../components/Map';
import {SelectSpot} from '../components/SelectSpot';

const { Navigator, Screen } = createNativeStackNavigator();

export function AppRoutes() {
    return (
        <Navigator screenOptions={{headerShown: false}}>
            <Screen name="map"
            component={Map}/>
            <Screen name="selectspot"
            component={SelectSpot}/>
        </Navigator>
    );
}
