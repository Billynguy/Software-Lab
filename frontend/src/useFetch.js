import { useState, useEffect} from 'react';

const useFetch = (url) => { // custom hooks in react need to start with word 'use'
    const [data, setData] = useState(null);
    const [isPending, setIsPending] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {                           // can't make this async
        const abortCont = new AbortController();


        fetch(url, { signal: abortCont.signal }) // associates abortCont with this fetch
            .then(res => {                      // 'then' fires a function once the fetch promise has resolved, ie once we have the data back. Reponse object res is NOT the data
                if(!res.ok){
                    throw Error('Could not fetch the data for that resource.') // Can connect to server but response is not normal
                }
                return res.json()               // passes the json into a javascript object, the 'return res.json()' returns a promise b/c res.json() is aync
            })
            .then(data => {                     // we get the data now   
                setData(data);
                setIsPending(false);
                setError(null); // gets rid of error message in (successful) subsequent requests
            })
            .catch(err => { // Catches any network error
                if (err.name === 'AbortError'){
                    console.log('Fetch Aborted');
                }
                else {
                    setIsPending(false);
                    setError(err.message);
                }
                
            })
        return () => abortCont.abort();       
        
    }, [url]); // whenever the url changes, this function will be rerun to get the data

    return { data, isPending, error}
}

export default useFetch;